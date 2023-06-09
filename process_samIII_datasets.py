#!/usr/bin/env python3
# process_datasets.py
# Hunter Barndt
# Purpose: Subtract each day's values in a year by the first value of the day

### CAN POSSIBLY COMBINE WITH process_gima_datasets.py ####

import pandas as pd
import time as tm
import numpy as np
import glob as gb

from define import current_machine
from define import directory_preambles
from define import processing_start_year
from define import processing_end_year 

### Global Variables ###
all_year_dataframes = []

# Only used for samIII datasets at the moment
dataset_types = [
    'samIII'
    #'gima'
]

### Prompts ###

# Select specific year to analyze
print(f"Which year would you like to process? [Option(s): {processing_start_year} thru {processing_end_year}]")
while True:
    selected_year = input()
    if int(selected_year) >= (processing_start_year) or int(selected_year) <= processing_end_year:
        selected_year = int(selected_year)
        break
    else:
        print("Enter valid year.")

# Select dataset to process
print(f"Which dataset would you like you process? [Option(s): Look at \"dataset_types\" list variable for options]")
print(f"Option(s): ")
for dataset in dataset_types:
    print(dataset)
while True:
    dataset_type = input()
    if dataset_type in dataset_types:
        break
    else:
        print("Enter valid year.")

### Functions ###

def getSelectedYearSubtractedData(df, components):
    
    # Subtract first reading from a day from all of it's days...
    df = df.reset_index()
    
    def subtractDayValues(date):
        df_day = df[ df['datetime'].dt.date == date ]
        for i in range(len(components)):
            df_day[components[i]] = df_day[components[i]] - df_day.iloc[0,i+1]
        return df_day
    
    dates = df.datetime.dt.date.unique()
    df_day_subbed = pd.DataFrame()
    sub_values = np.vectorize(subtractDayValues)
    df_subbed_days_dataframes = sub_values(dates)
    for subbed_day in df_subbed_days_dataframes:
        df_day_subbed = pd.concat([df_day_subbed, subbed_day])
    
    return df_day_subbed

### Main ###

def main():
    # Declare pickle and csv output directories
    pickle_path_name = f"{directory_preambles[current_machine]}pickles/{dataset_type}/{selected_year}-{dataset_type.upper()}-Processed-Data.pickle"
    #csv_path_name = f"{directory_preambles[current_machine]}csvs/{dataset_type}/{selected_year}-{dataset_type.upper()}-Processed-Data.csv"

    # Get database directory
    glob_database_dir = f"{directory_preambles[current_machine]}pickles/{dataset_type}/*-{dataset_type.upper()}-Data.pickle"
    database_dir_list = gb.glob(glob_database_dir)
    dateformat = "%d.%m.%Y %H:%M:%S"

    # Get all available yearly databases
    for database in database_dir_list:
        temp_dataframe = pd.read_pickle(database)
        all_year_dataframes.append(temp_dataframe)
    selected_year_path = f"{directory_preambles[current_machine]}pickles/{dataset_type}/{selected_year}-{dataset_type.upper()}-Data.pickle"
    
    # Define components measured by magnetometer
    components = ['x', 'y', 'z']

    selected_year_dataframe = pd.read_pickle(selected_year_path)
    selected_year_dataframe_subbed = getSelectedYearSubtractedData(selected_year_dataframe, components)
    # Calculates horizontal component
    selected_year_dataframe_subbed['H'] = np.sqrt(selected_year_dataframe_subbed['x'] ** 2 + selected_year_dataframe_subbed['y'] ** 2)
    # Calculates declination component with respect to the true north magnetic field
    selected_year_dataframe_subbed['D'] = np.arctan2(selected_year_dataframe_subbed['y'], selected_year_dataframe_subbed['x'])
    # Calculates the absolute value differential in H
    selected_year_dataframe_subbed['dH'] = np.abs(selected_year_dataframe_subbed['H'].diff())
    # Calculates the differential in time
    selected_year_dataframe_subbed['dt'] = selected_year_dataframe_subbed.index.to_series().diff().dt.total_seconds()
    # Calculates the change of H in time
    selected_year_dataframe_subbed['dHdt'] = selected_year_dataframe_subbed['dH'] / selected_year_dataframe_subbed['dt']
    selected_year_dataframe_subbed.to_pickle(pickle_path_name)
    #selected_year_dataframe_subbed.to_csv(pickle_path_name)

    
start_time = tm.time()
main()
end_time = tm.time()
print(f"Time to Excecute: {end_time-start_time} s")