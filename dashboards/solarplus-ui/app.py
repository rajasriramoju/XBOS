from flask import Flask, request, send_from_directory
from flask import make_response, request, current_app
from flask import jsonify, redirect, url_for
from datetime import timedelta
from functools import update_wrapper
from Influx_Client import Influx_Dataframe_Client
from influxdb import InfluxDBClient
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
    ciee = pd.csv("./sample_data/ciee.csv")
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

'''
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
'''

# Connect to InfluxDB
@app.route('/influxdb')
@crossdomain(origin="*")
def extract_data_influxdb():
    """ Extract data from InfluxDB.

    Note
    ----
    Need config file for InfluxDB connection.

    Returns
    -------
    json
        Json containing temperature data from InfluxDB.

    """

    # Influx_Client is a python wrapper around InfluxDB
    # Check https://github.com/akshephard/Influx_Dataframe_Client for more details

    '''For Tempterature.csv'''
    '''
    readDF = pd.read_csv('Temperature.csv')
    #readDf.a.str.contains(na = False)
    print("read the csv file")
    #print(readDF)
    #tags_list = []
    fields_list = readDF.columns
    print("these are fields: ", readDF.columns)
    database = 'temperatureDB'
    measurement = readDF.values
    print("got the measurement values: ",readDF.values)


    # Create Influx DB Client
    client = Influx_Dataframe_Client(config_file = 'config.yaml')
    print("created the client")
    #df[readDF.columns].replace('', np.nan, inplace = True)
    #print("replaced to nan")
    #dbClient = InfluxDBClient(host='localhost', port='8086', user='Admin',
    #                        password='password', database='temperatureDB')
    #df = dbCient.create_database(database)
    #client = InfluxDBClient(database = 'temperatureDB', host='localhost:5000', port = 8086)

    # Query temperature data
    #df = client.specific_query(measurement='temperature')

    #df = client.__post_to_DB(database = 'myDB')
    #df = client.write_dataframe(tags = readDF.columns, fields = readDF[:])
    df = client.write_csv('Temperature.csv', fields_list, measurement, database)
    print("wrote to csv")
    #df = client.write_json(json,database)
    #df = client.write_dataframe(data,tags_list,fields_list,measurement,database)
    #df = client.write_json(csv_fileName = file_path, tags = readDF.columns, fields = readDF[:])


    return df.to_json(orient='records')
    '''

    readDF = pd.read_csv('avenal-public-works-yard.csv')
    print("read the csv file")


    fields_list = readDF.columns[1:]
    print("these are fields: ", fields_list)

    database = 'avenal_public_works_yard_DB'
    print("database: ", database)

    measurement_values = readDF.values[:]
    measurement = 'avenal-public-works-yard'
    #measurement = measurement_values[:,1:]

    print("got the measurement values: ", measurement)


    # Create Influx DB Client
    client = Influx_Dataframe_Client(config_file = 'config_avelnal.yaml')
    print("created the client")
    #df[readDF.columns].replace('', np.nan, inplace = True)
    #print("replaced to nan")

    # Query temperature data
    #df = client.specific_query(measurement='temperature')
    df = client.write_csv('avenal-public-works-yard.csv',
                            fields_list, measurement, database)
    print("wrote to db")



    return df.to_json(orient='records')

def create_app():
    app = Flask(__name__)

    with app.app_context():
        extract_data_influxdb()

    return app

if __name__ == '__main__':
    app.run()
