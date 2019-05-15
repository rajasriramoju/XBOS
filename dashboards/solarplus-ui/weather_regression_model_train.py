from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

def createDataTable():
	df_temperature =pd.read_csv('./Historic_microgrid_data/AirTemperatureData.csv')
	df_PVPower = pd.read_csv('./Historic_microgrid_data/PVPowerGenData.csv')

	# eliminating all entries except for the ones in the time range 
	# we are looking from 14th march to 24th april 2018
	# 2018-03-14 -> 2018-04-24
	


	temperature_lastIndex = df.temperature
	#having a while loop that runs till the temperature dataframe is empty
	while(df_temperature.empty == false):

		startDateEntries = cieeDF[cieeDF['TimeStamp'].str.contains(startDate)]