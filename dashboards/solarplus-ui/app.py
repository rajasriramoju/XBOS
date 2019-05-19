def application(environ, start_response):
  if environ['REQUEST_METHOD'] == 'OPTIONS':
    start_response(
      '200 OK',
      [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Credentials', 'true'),
        ('Access-Control-Allow-Headers', 'Authorization, Content-Type'),
        ('Access-Control-Allow-Methods', 'POST'),
      ]
    )
    return ''

from flask import Flask, request, send_from_directory
import config
from flask import make_response, request, current_app
from flask import jsonify, redirect, url_for
from flask import g, render_template, url_for, session

from datetime import timedelta
from functools import update_wrapper 
import pandas as pd 
import datetime
from flask_oidc import OpenIDConnect
from okta import UsersClient

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"
app.config["OIDC_COOKIE_SECURE"] = False
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.config["SECRET_KEY"] = config.secret_key
app.config["OIDC_ID_TOKEN_COOKIE_NAME"] = "oidc_token"
oidc = OpenIDConnect(app)
okta_client = UsersClient(config.org_url, config.token)



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

@app.route("/index")
@oidc.require_login
def index():
    """
    Render the homepage.
    """
    return render_template('index.html')

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
    return render_template("setpoints.html")

@app.route("/weather")
@oidc.require_login
def weather():
    """
    Render the weather page.
    """
    return render_template("weather.html")

@app.route("/DR")
@oidc.require_login
def dr():
    """
    Render the DR page.
    """
    return render_template("DR.html")

@app.route("/intelligence")
@oidc.require_login
def intelligence():
    """
    Render the intelligence page.
    """
    return render_template("intelligence.html")


@app.route("/login")
@oidc.require_login
def login():
    """
    Force the user to login, then redirect them to the dashboard.
    """
    return redirect(url_for(".index"))

@app.route("/logout")
def logout():
    """
    Log the user out of their account.
    """

    oidc.logout()
    return redirect(url_for(".landing"))

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

# This function extracts data for any feature's data from Control.csv data
# of the solarplus sample data -> will be used for total power consumption 
# values for dashboard
@app.route('/dashboard/access/<feature1>')
@crossdomain(origin="*")
def extractData_oneFeature_Control2(feature1):
    filePathString = "./solarplus_sample_data/Conrol2.csv"
    readDF = pd.read_csv(filePathString)

    df = readDF[:,'Time',feature1]
    return df.to_json(orient = 'records')

# This function extracts data for any 2 features' data from Control.csv data
# of the solarplus sample data -> will be used for HVAC1 and HVAC2 
# values for dashboard
@app.route('/dashboard/access/<feature1>/<feature2>')
@crossdomain(origin="*")
def extractData_twoFeatures_Control2(feature1, feature2):
    filePathString = "./solarplus_sample_data/Conrol2.csv"
    readDF = pd.read_csv(filePathString)

    df = readDF[:,'Time',feature1,feature2]
    return df.to_json(orient = 'records')

# This function extracts data for solar production values from 
@app.route('/dashboard/PVPowerGenData')
@crossdomain(origin="*")
def extractData_PVPowerGenData():
    filePathString = "./Historic_microgrid_data/PVPowerGenData.csv"
    readDF = pd.read_csv(filePathString)

    df = readDF[:,'Date_PT','PVPower_kW']
    return df.to_json(orient = 'records')


# if __name__ == '__main__':
#     app.run()
#     debug=True
#     TEMPLATES_AUTO_RELOAD=True
