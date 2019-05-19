from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

def createDataTable():
	df_temperature =pd.read_csv('./Historic_microgrid_data/AirTemperatureData.csv')
	df_PVPower = pd.read_csv('./Historic_microgrid_data/PVPowerGenData.csv')

	# eliminating all entries except for the ones in the time range 
	# we are looking from 14th march to 24th april 2018
	# 2018-03-14 -> 2018-04-24
	startDate = "2018-03-14"
	endDate = "2018-04-24"

	# For temperature data
	# This gets all the entries of the specific start date and end date
	startDateEntries_temperature = df_temperature[df_temperature['Date_PT'].str.contains(startDate)]
	endDateEntries_temperature = df_temperature[df_temperature['Date_PT'].str.contains(endDate)]

    # finding the first index of start date entries and last index of the end date entries
    # so that we can get the range of indices for the data in the specified timeframe
	startDateIndex_temperature = startDateEntries_temperature.index[0]
	endDateIndex_temperature = endDateEntries_temperature.index[-1]

    #fetching data in the specific timeframe
	dataInRange_temperature = df_temperature[startDateIndex_temperature:(endDateIndex_temperature+1)]

	# Repeating the same process for PVPower Data
	startDateEntries_power = df_PVPower[df_PVPower['Date_PT'].str.contains(startDate)]
	endDateEntries_power = df_PVPower[df_PVPower['Date_PT'].str.contains(endDate)]
	startDateIndex_power = startDateEntries_power.index[0]
	endDateIndex_power = endDateEntries_power.index[-1]
	dataInRange_power = df_PVPower[startDateIndex_power:(endDateIndex_power+1)]

	nextEntryIndex_power = df_PVPower.index[0]
	df_model = pd.DataFrame() #creating an epty dataframe that feeds to model
	df_model = pd.DataFrame(columns=['date', 'AirTemp_degC_Max', 'PVPower_kW_Sum'])
	#df_model = pd.DataFrame(columns=['AirTemp_degC_Max', 'PVPower_kW_Sum'])

	#print(dataInRange_temperature)
	#print(dataInRange_power)
	
	#having a while loop that runs till the power dataframe is empty since that is shorter
	while not dataInRange_power.empty:
	#for x in range(4):
		# getting the date of the entry we want to deal with
		#print(df_PVPower.iloc[df_PVPower.index[0]]) #[nextEntryIndex_power])
		currDateEntry = dataInRange_power.iloc[nextEntryIndex_power].Date_PT
		currDate = (currDateEntry.split(' '))[0]
		print(currDateEntry)

		#obtaining max temperature of a day
		currDateEntries_temperature = dataInRange_temperature[dataInRange_temperature['Date_PT'].str.contains(currDate)].AirTemp_degC
		currDateEntriesTempMax = max(currDateEntries_temperature)

		#obtaining sum power production of a day
		currDateEntries_power = dataInRange_power[dataInRange_power['Date_PT'].str.contains(currDate)].PVPower_kW
		currDateEntriesPowerSum = sum(currDateEntries_power)

		df_model.loc[len(df_model)] = [currDate, currDateEntriesTempMax, currDateEntriesPowerSum]
		#df_model.loc[len(df_model)] = [currDateEntriesTempMax, currDateEntriesPowerSum]

		dataInRange_power = dataInRange_power[~dataInRange_power.Date_PT.str.contains(currDate)]
		print(dataInRange_power)
		print("going onto next iteration")
		print(df_model)

		# finding the next date to perform the same operations on, as long as the dataframe is not alraedy empty
		if not dataInRange_power.empty:
			nextEntryIndex_power = dataInRange_power.index[0]
			print("next entry = ", nextEntryIndex_power)
	
	print(df_model)




createDataTable()
