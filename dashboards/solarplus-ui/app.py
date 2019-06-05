from flask import Flask, request, send_from_directory, json
import config
from flask import make_response, request, current_app
from flask import jsonify, redirect, url_for
from flask import g, render_template, url_for, session
from influxdb import InfluxDBClient, DataFrameClient
import argparse
import boto3
import boto.ses
import base64
from venstar_driver import Venstar_Driver 
from urllib.request import urlopen
import json
import requests

from datetime import timedelta
from functools import update_wrapper
import pandas as pd
import datetime
from flask_oidc import OpenIDConnect
from okta import UsersClient

from sklearn.linear_model import LinearRegression
from sklearn import model_selection
import pickle
import numpy as np
from json import dumps



AWS_ACCESS_KEY = config.aws_access_key
AWS_SECRET_KEY = config.aws_secret_key

obj = Venstar_Driver("config.yaml")

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': config.secret_key,
    'OIDC_CLIENT_SECRETS': './client_secrets.json',
    'OIDC_DEBUG': True,
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_SCOPES': ["openid", "profile","email"],
    'OIDC_CALLBACK_ROUTE': '/authorization-code/callback',
    "OIDC_ID_TOKEN_COOKIE_NAME": 'oidc_token'
})
# app.config["DEBUG"] = True
# app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"
# app.config["OIDC_COOKIE_SECURE"] = False
# app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
# app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
# app.config["SECRET_KEY"] = config.secret_key
# app.config["OIDC_ID_TOKEN_COOKIE_NAME"] = "oidc_token"





oidc = OpenIDConnect(app)
okta_client = UsersClient(config.org_url, config.token)

class Email(object):
        def __init__(self, to, subject):
            self.to = to
            self.subject = subject
            self._html = None
            self._text = None
            self._format = 'html'

        def html(self, html):
            self._html = html

        def text(self, text):
            self._text = text

        def send(self, from_addr=None):
            body = self._html

            if isinstance(self.to, str):
                self.to = [self.to]
            if not from_addr:
                from_addr = 'webwizards193@gmail.com'
            if not self._html and not self._text:
                raise Exception('You must provide a text or html body.')
            if not self._html:
                self._format = 'text'
                body = self._text

            connection = boto.ses.connect_to_region(
                'us-west-2',
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_KEY
            )

            return connection.send_email(
                from_addr,
                self.subject,
                None,
                self.to,
                format=self._format,
                text_body=self._text,
                html_body=self._html
            )

# Create an SNS client
client = boto3.client(
"sns",
aws_access_key_id=AWS_ACCESS_KEY,
aws_secret_access_key=AWS_SECRET_KEY,
region_name="us-west-2"
)

@app.before_request
def before_request():
    """
    Load a proper user object using the user ID from the ID token. This way, the
    `g.user` object can be used at any point.
    """
    if oidc.user_loggedin:
        g.user = okta_client.get_user(oidc.user_getfield("sub"))
    else:
        g.user = None



@app.route("/")
def landing():
    """
    Render the landing page.
    """
    return render_template('landing.html')

# @app.route("/index")
# @oidc.require_login
# def index():

#     """
#     Render the homepage.
#     """
#     return render_template('index.html')

@app.route("/dashboard")
@oidc.require_login
def dashboard():
    """
    Render the dashboard page.
    """
    return render_template("dashboard.html")

@app.route("/setpoints")
@oidc.require_login
def setpoints():
    """
    Render the setpoints page.
    """
    # create the client for influxdb
    client = InfluxDBClient('127.0.0.1', 8086,'setpoints_db')
    client.switch_database('setpoints_db')

    queryTemp1 = client.query('SELECT "Thermostat1_HSP" from temperature ORDER BY DESC LIMIT 1')
    points1 = queryTemp1.get_points()
    for item in points1:
            result1 = item['Thermostat1_HSP']

    queryTemp2 = client.query('SELECT "Thermostat1_CSP" from temperature ORDER BY DESC LIMIT 1')
    points2 = queryTemp2.get_points()
    for item in points2:
            result2 = item['Thermostat1_CSP']

    queryTemp3 = client.query('SELECT "Thermostat2_HSP" from temperature ORDER BY DESC LIMIT 1')
    points3 = queryTemp3.get_points()
    for item in points3:
            result3 = item['Thermostat2_HSP']

    queryTemp4 = client.query('SELECT "Thermostat2_CSP" from temperature ORDER BY DESC LIMIT 1')
    points4 = queryTemp4.get_points()
    for item in points4:
            result4 = item['Thermostat2_CSP']

    queryTemp5 = client.query('SELECT "Refrigerator_SP" from temperature ORDER BY DESC LIMIT 1')
    points5 = queryTemp5.get_points()
    for item in points5:
            result5 = item['Refrigerator_SP']

    queryTemp6 = client.query('SELECT "Refrigerator_SP+dT" from temperature ORDER BY DESC LIMIT 1')
    points6 = queryTemp6.get_points()
    for item in points6:
            result6 = item['Refrigerator_SP+dT']
            print(result6)

    queryTemp7 = client.query('SELECT "Freezer_SP" from temperature ORDER BY DESC LIMIT 1')
    points7 = queryTemp7.get_points()
    for item in points7:
            result7 = item['Freezer_SP']

    queryTemp8 = client.query('SELECT "Freezer_SP+dT" from temperature ORDER BY DESC LIMIT 1')
    points8 = queryTemp8.get_points()
    for item in points8:
            result8 = item['Freezer_SP+dT']

    '''return render_template("setpoints.html",temperature1=result1,temperature2=result2,
                            temperature3=result3,temperature4=result4,temperature5=result5,
                            temperature6=result6,temperature7=result7,temperature8=result8)'''
    if g.user.id == '00uj9ow24kHWeZLwN356':
        
        return render_template("setpoints.html",temperature1=result1,temperature2=result2,
                                temperature3=result3,temperature4=result4,temperature5=result5,
                                temperature6=result6,temperature7=result7,temperature8=result8)
    else:
        return render_template('404.html'), 404

@app.route("/weather")
@oidc.require_login
def weather():
    """
    Render the weather page.
    """
    return render_template("weather.html")

@app.route("/analysis")
@oidc.require_login
def analysis():
    """
    Render the weather page.
    """
    if g.user.id == '00uj9ow24kHWeZLwN356':
        return render_template("analysis.html")
    else:
        return render_template('404.html'), 404


# @app.route("/DR")
# @oidc.require_login
# def dr():
#     """
#     Render the DR page.
#     """
#     return render_template("DR.html")

@app.route("/intelligence")
@oidc.require_login
def intelligence():
    """
    Render the intelligence page.
    """
    if g.user.id == '00uj9ow24kHWeZLwN356':
        return render_template("intelligence.html")
    else:
        return render_template('404.html'), 404


@app.route("/contact")
@oidc.require_login
def contact():
    """
    Render the intelligence page.
    """
    return render_template("contact.html", email=g.user.profile.email)

@app.route("/profile")
@oidc.require_login
def profile():
    """
    Render the intelligence page.
    """
    return render_template("profile.html", user=g.user.id)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route("/login")
def login():
    bu = oidc.client_secrets['issuer'].split('/oauth2')[0]
    cid = oidc.client_secrets['client_id']

    destination = 'http://127.0.0.1:5000/dashboard'
    state = {
        'csrf_token': session['oidc_csrf_token'],
        'destination': oidc.extra_data_serializer.dumps(destination).decode('utf-8')
    }

    return render_template("login.html", oidc=oidc, baseUri=bu, clientId=cid, state=base64.urlsafe_b64encode(json.dumps(state).encode('UTF-8')).decode('ascii'))

@app.route("/logout")
def logout():
    oidc.logout()

    return redirect(url_for(".landing"))




# @app.route("/login")
# @oidc.require_login
# def login():
#     """
#     Force the user to login, then redirect them to the dashboard.
#     """
#     return redirect(url_for(".index"))

# @app.route("/logout")
# def logout():
#     """
#     Log the user out of their account.
#     """

#     oidc.logout()
#     return redirect(url_for(".landing"))

@app.route('/setpoints/thermostat', methods=['POST'])
def thermostat():
    response = request.get_json()
    temp1 = response["temp1"]
    temp2 = response["temp2"]
    temp3 = response["temp3"]
    temp4 = response["temp4"]

    print(temp1)
    print(temp2)
    print(temp3)
    print(temp4)
    obj.controls(heattemp=temp1,cooltemp=temp2)
    return jsonify({"message": "done"})

@app.route('/aws', methods=['POST'])
def aws():
    # Send your sms message.
    response = request.get_json()
    print(response)
    print(response["name"])
    print(response["email"])
    print(response["number"])
    print(response["message"])
    client.publish(
    PhoneNumber="+1" + str(response["number"]),
    Message="Hi, " + str(response["name"]) + ": Your Solarplus Issue Ticket has been received!  Thank you! :)"
    )

    email = Email(to='webwizards193@gmail.com', subject='New Issue Ticket Posted!')
    email.text('This is a text body. Foo bar.')
    email.html('<html><body>''Dear Admin <br>' + str(response["name"]) + ' says:<br>' + '<strong>' + str(response["message"]) +'</strong> </body></html>')  # Optional
    email.send()

    return jsonify({"message": "done"})


# @app.before_request
# def before_request():
#     """
#     Load a proper user object using the user ID from the ID token. This way, the
#     `g.user` object can be used at any point.
#     """
#     if oidc.user_loggedin:
#         g.user = okta_client.get_user(oidc.user_getfield("sub"))
#     else:
#         g.user = None


# @app.route('/')
# def root():
#     return render_template('index.html')



# @app.route("/login")
# @oidc.require_login
# def login():
#     """
#     Force the user to login, then redirect them to the dashboard.
#     """
#     return render_template('dashboard.html')

# @app.route('/<path:path>')
# @oidc.require_login
# def static_proxy(path):
#     return render_template(path)

# @app.route("/logout")
# @oidc.require_login
# def logout():
#     """
#     Log the user out of their account.
#     """

#     oidc.logout()
#     return redirect(url_for(".root"))


# Flask boilerplate,
# configure CORS to make HTTP requests from javascript
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route('/cieeData')
@crossdomain(origin="*")
def cieeData():
    ciee = pd.read_csv("./sample_data/ciee.csv")
    ciee.columns = ['TimeStamp', 'ciee', 's0', 's1', 's2', 's3']

    #limiting to 20 entries like prev demo
    ciee = ciee[:20]

    return ciee.to_json(orient='records')


@app.route('/cieeData/<startDate>/<endDate>')
@crossdomain(origin="*")
def extractData(startDate, endDate):
    cieeDF = pd.read_csv("./sample_data/ciee.csv")
    cieeDF.columns = ['TimeStamp', 'ciee', 's0', 's1', 's2', 's3']

    # check for validity of range of dates
    startYear,startMonth,startDay=[int(x) for x in startDate.split('-')]
    endYear,endMonth,endDay=[int(x) for x in endDate.split('-')]

    if(datetime.datetime(startYear,startMonth,startDay) > datetime.datetime(endYear,endMonth,endDay)):
        print ('Wrong range of dates given. Start Date = ' ,startDate, "; End Date = ", endDate)
        return 'Incorrect Range of dates'

    # This gets all the entries of the specific start date and end date
    startDateEntries = cieeDF[cieeDF['TimeStamp'].str.contains(startDate)]
    endDateEntries = cieeDF[cieeDF['TimeStamp'].str.contains(endDate)]

    # finding the first index of start date entries and last index of the end date entries
    # so that we can get the range of indices for the data in the specified timeframe
    startDateIndex = startDateEntries.index[0]
    endDateIndex = endDateEntries.index[-1]

    #fetching data in the specific timeframe
    dataInRange = cieeDF[startDateIndex:(endDateIndex+1)]
    #print(dataInRange)

    return dataInRange.to_json(orient = 'records')


# This function takes in a file name, start and end date with the two features that
# the user wants plotted on the graph
@app.route('/<filename>/<startDate>/<endDate>/<feature1>/<feature2>')
@crossdomain(origin="*")
def extractData_plotTwoQueries(filename, startDate, endDate, feature1, feature2):

    filePathString = "./solarplus_sample_data/" + filename+".csv"
    print(filePathString)
    readDF = pd.read_csv(filePathString)

    '''The names the columns of the data frame using the first row info - assumes that column names
     are entered correctly in the csv files - which is why the column names are not renamed in this
     function. '''

    # check for validity of range of dates
    startYear,startMonth,startDay=[int(x) for x in startDate.split('-')]
    endYear,endMonth,endDay=[int(x) for x in endDate.split('-')]

    if(datetime.datetime(startYear,startMonth,startDay) > datetime.datetime(endYear,endMonth,endDay)):
        print ('Wrong range of dates given. Start Date = ' ,startDate, "; End Date = ", endDate)
        return 'Incorrect Range of dates'


    # This gets all the entries of the specific start date and end date
    startDateEntries = readDF[readDF['Time'].str.contains(startDate)]
    endDateEntries = readDF[readDF['Time'].str.contains(endDate)]

    # finding the first index of start date entries and last index of the end date entries
    # so that we can get the range of indices for the data in the specified timeframe
    startDateIndex = startDateEntries.index[0]
    endDateIndex = endDateEntries.index[-1]

    #fetching data in the specific timeframe
    dataInRange = readDF[startDateIndex:(endDateIndex+1)]

    dataInRange = dataInRange.loc[:,['Time', feature1, feature2]]

    return dataInRange.to_json(orient = 'records')



@app.route('/setpoints/getEntry1', methods = ['POST'])
def renderFirstRow1():
    content = request.get_json(silent=False, force=True)
    Thermostat1_HSP = content['temp1']
    #print("Thermostat1_HSP: ", Thermostat1_HSP)

    Thermostat1_CSP = content['temp2']
    #print("Thermostat1_CSP: ", Thermostat1_CSP)

    Thermostat2_HSP = content['temp3']
    #print("Thermostat2_HSP: ", Thermostat2_HSP)

    Thermostat2_CSP = content['temp4']
    #print("Thermostat2_CSP: ", Thermostat2_CSP)


    # inserting data into the database
    client = InfluxDBClient('127.0.0.1', 8086, 'setpoints_db')
    client.switch_database('setpoints_db')

    json_body = [{
        'tags': {
            'User':'username'
            },
        'fields': {
            'Thermostat1_HSP': Thermostat1_HSP,
            'Thermostat1_CSP': Thermostat1_CSP,
            'Thermostat2_HSP': Thermostat2_HSP,
            'Thermostat2_CSP': Thermostat2_CSP
            },
        'measurement': 'temperature'
        }]

    client.write_points(json_body)

    return "success"


@app.route('/setpoints/getEntry2', methods = ['POST'])
def renderFirstRow2():
    content = request.get_json(silent=False, force=True)
    Refrigerator_SP = content['temp5']
    #print("Refrigerator_SP: ", Refrigerator_SP)

    Refrigerator_SP_Plus_dT = content['temp6']
    #print("Refrigerator_SP_Plus_dT: ", Refrigerator_SP_Plus_dT)

    Freezer_SP = content['temp7']
    #print("Freezer_SP: ", Freezer_SP)

    Freezer_SP_Plus_dT = content['temp8']
    #print("Freezer_SP_Plus_dT: ", Freezer_SP_Plus_dT)

    client = InfluxDBClient('127.0.0.1', 8086, 'setpoints_db')
    client.switch_database('setpoints_db')

    json_body = [{
        'tags': {
            'User':'username'
            },
        'fields': {
            'Refrigerator_SP': Refrigerator_SP,
            'Refrigerator_SP+dT': Refrigerator_SP_Plus_dT,
            'Freezer_SP': Freezer_SP,
            'Freezer_SP+dT': Freezer_SP_Plus_dT
            },
        'measurement': 'temperature'
        }]

    client.write_points(json_body)

    return "success"


@app.route('/analysis/MLModel/<day1>/<day2>/<day3>/<day4>/<day5>/<day6>/<day7>')
@crossdomain(origin="*")
def MLPredictionModel(day1, day2, day3, day4, day5, day6, day7):
    print(day1, day2, day3, day4, day5, day6, day7)
    filename = 'trained_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    X_pred = [[float(day1)],[float(day2)],[float(day3)],[float(day4)],[float(day5)],[float(day6)],[float(day7)]]
    Y_pred =  loaded_model.predict(X_pred)

    print(X_pred)
    print(Y_pred)

    X_pred=[float(day1), float(day2), float(day3), float(day4), float(day5), float(day6), float(day7)]
    dataset = pd.DataFrame({'X_pred': X_pred, 'Column1':Y_pred})
    #dataset = pd.DataFrame.from_records(Y_pred)

    #print(Y_pred[0])
    print(dataset)
    #Y_pred0 = {'temperature': Y_pred[0]}

    #return make_response(dumps(Y_pred))

    return dataset.to_json(orient = 'records')

# This function extracts data for any feature's data from Control.csv data
# of the solarplus sample data -> will be used for total power consumption
# values for dashboard
@app.route('/dashboard/access/<feature1>')
@crossdomain(origin="*")
def extractData_oneFeature_Control2(feature1):
    filePathString = "./solarplus_sample_data/Control2.csv"
    readDF = pd.read_csv(filePathString)

    df = readDF.loc[:,['Time',feature1]]
    return df.to_json(orient = 'records')

# This function extracts data for any 2 features' data from Control.csv data
# of the solarplus sample data -> will be used for HVAC1 and HVAC2
# values for dashboard
@app.route('/dashboard/access/<feature1>/<feature2>')
@crossdomain(origin="*")
def extractData_twoFeatures_Control2(feature1, feature2):
    filePathString = "./solarplus_sample_data/Control2.csv"
    readDF = pd.read_csv(filePathString)

    df = readDF.loc[:,['Time',feature1,feature2]]
    return df.to_json(orient = 'records')

# This function extracts data for solar production values from
@app.route('/dashboard/PVPowerGenData')
@crossdomain(origin="*")
def extractData_PVPowerGenData():
    filePathString = "./Historic_microgrid_data/PVPowerGenData.csv"
    readDF = pd.read_csv(filePathString)

    df = readDF.loc[:,['Date_PT','PVPower_kW']]
    return df.to_json(orient = 'records')

# This function extracts data for any feature's data from Control.csv data
# of the solarplus sample data -> will be used for average power consumption
# values
@app.route('/dashboard/access/<feature1>/average')
@crossdomain(origin="*")
def extractData_oneFeature_Control3(feature1):
    filePathString = "./solarplus_sample_data/Control2.csv"
    readDF = pd.read_csv(filePathString)

    df = readDF.loc[:,['Time',feature1]]

    # loop here to go through the dataframe and calculate the average
    nextEntryIndex = df.index[0]
    df_model = pd.DataFrame() #creating an epty dataframe that feeds to model
    df_model = pd.DataFrame(columns=['Time', feature1])

    print(df)

	#having a while loop that runs till the power dataframe is empty since that is shorter
    while not df.empty:
        # getting the date of the entry we want to deal with
        currDateEntry = df.iloc[nextEntryIndex].Time
        currDate = (currDateEntry.split(' '))[0]
        print(currDateEntry)
        
        #obtaining average power production of a day
        currDateEntries_power = df[df['Time'].str.contains(currDate)].Building
        currDateEntriesPowerAverage = sum(currDateEntries_power)/len(currDateEntries_power)
        df_model.loc[len(df_model)] = [currDate, currDateEntriesPowerAverage]
        
        df = df[~df.Time.str.contains(currDate)]
        # finding the next date to perform the same operations on, as long as the dataframe is not alraedy empty
        if not df.empty:
            nextEntryIndex_power = df.index[0]
        
    print(df_model)

    return df_model.to_json(orient = 'records')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
