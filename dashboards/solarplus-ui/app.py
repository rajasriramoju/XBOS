from flask import Flask, request, send_from_directory
from flask import make_response, request, current_app
from flask import jsonify, redirect, url_for
from datetime import timedelta
from functools import update_wrapper
from influxdb import InfluxDBClient
from influxdb import DataFrameClient
import pandas as pd
import datetime

app = Flask(__name__)
app.debug = True

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

@app.route('/')
def root():
    return app.send_static_file('login.html')

@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)

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




# This function takes in a file name, start and end date and returns json response
@app.route('/<filename>/<startDate>/<endDate>')
@crossdomain(origin="*")
def extractData_anyFile(filename, startDate, endDate):

    filePathString = "./solarplus_sample_data/" + filename + ".csv"
    print(filePathString)
    readDF = pd.read_csv(filePathString)


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

    return dataInRange.to_json(orient = 'records')


@app.route('/setpoints/set/<T1Min>/<T1Max>/<T2Min>/<T2Max>/<T3Min>/<T3Max>/<T4Min>/<T4Max>/<username>')
@crossdomain(origin="*")
def setValuesInDB(T1Min, T1Max, T2Min, T2Max, T3Min, T3Max, T4Min, T4Max, username):
    client = InfluxDBClient(host='127.0.0.1', port=5000)
    #client.create_database('setpoints_db')
    client.switch_database('setpoints_db')


    json_body = [
    {
        "measurement": "temperature",
        "tags": {
            "User": username,
            "Thermostat1_HSP": T1Min,
            "Thermostat1_CSP": T1Max,
            "Thermostat2_HSP": T2Min,
            "Thermostat2_CSP": T2Max,
            "Refrigerator_SP": T3Min,
            "Thermostat1_SP+dT": T3Max,
            "Freezer_SP": T4Min,
            "Freezer_SP+dT": T4Max
                }
    }]
    client.write_points(json_body)

@app.route('/setpoints/get/<T1Min>/<T1Max>/<T2Min>/<T2Max>/<T3Min>/<T3Max>/<T4Min>/<T4Max>/<username>')
@crossdomain(origin="*")
def renderFirstRow():
    dfClient = influxdb.DataFrameClient(host='127.0.0.1', port=5000)
    #getting only the first row
    dfClient.query("""SELECT "Thermostat1_HSP", "Thermostat1_CSP", "Thermostat2_HSP",
                    "Thermostat2_CSP", "Refrigerator_SP", "Thermostat1_SP+dT",
                    "Freezer_SP", "Freezer_SP+dT" from setpoints_db
                    ORDER BY DESC LIMIT 1""")


# pass in as json (to-json)


if __name__ == '__main__':
    app.run()
