#!/usr/bin/env python3
# preprocess_gima_csvs.py
# Hunter Barndt
# Purpose: Subtract each day's values in a year by the first value of the day

import pandas as pd
import time as tm
import numpy as np
import glob as gb

### Global Variables ###
#start_year = 2009
start_year = 2010
end_year = 2022
num_years = end_year - start_year

gima_sites = [
    'trapper_creek'
]

# Select specific year to analyze
print(f"Which year would you like to process? [Option(s): {start_year} thru {end_year}]")
while True:
    selected_year = input()
    if int(selected_year) >= (start_year) or int(selected_year) <= end_year:
        selected_year = int(selected_year)
        break
    else:
        print("Enter valid year.")
        
# Select site to analyze
print(f"Which site would you like to process? ")
print(f"Option(s): ")
for site in gima_sites:
    print(site)
while True:
    selected_site = input()
    if selected_site in gima_sites:
        break
    else:
        print("Enter valid site.")

# Declare pickle and csv output directories
pickle_path_name = f"D:/UAF/PHYS Capstone/pickles/gima/{selected_year}-GIMA-Processed-Data.pickle"
csv_path_name = f"D:/UAF/PHYS Capstone/csvs/gima/{selected_year}-GIMA-Processed-Data.csv"

# Get csv directory
glob_csv_year_dir = f"D:/UAF/PHYS Capstone/GIMA_Data/{selected_site}/{selected_year}/*.csv"
csv_year_dir_list = gb.glob(glob_csv_year_dir)
dateformat = "%Y_%m_%d %H:%M:%S"
column_names = ['time', 'time-d', 'x', 'y', 'z']
drop_cols = ['time', 'time-d']

### Functions ###

def subtractDayValues(components, df, date):
    df_day = df[ df['datetime'].dt.date == date ]
    for i in range(len(components)):
        df_day[components[i]] = df_day[components[i]] - df_day.iloc[0,i+1]
    return df_day

### Main ###

def main():
    components = ['x', 'y', 'z']
    year_dataframe = pd.DataFrame()
    
    for day in csv_year_dir_list:
        dir_substring = day[39:49]
        day_dataframe = pd.read_csv(day, names=column_names)
        day_dataframe['datetime'] = pd.to_datetime(dir_substring + " " + day_dataframe['time'], format=dateformat)
        day_dataframe = day_dataframe.drop(columns=drop_cols)
        # Subtracts the first value of the day to all the readings of the day
        for i in range(len(components)):
            day_dataframe[components[i]] = day_dataframe[components[i]] - day_dataframe.iloc[0,i]
        # Calculates horizontal component
        day_dataframe['H'] = np.sqrt(day_dataframe['x'] ** 2 + day_dataframe['y'] ** 2)
        # Calculates declination component with respect to the true north magnetic field
        day_dataframe['D'] = np.arctan2(day_dataframe['y'], day_dataframe['x'])
        year_dataframe = pd.concat([year_dataframe, day_dataframe])
        
    print(f"Size of Dataframe: {year_dataframe.size}")
    #year_dataframe.to_csv(csv_path_name)
    year_dataframe.to_pickle(pickle_path_name)
    
start_time = tm.time()
main()
end_time = tm.time()
print(f"Time to Excecute: {end_time-start_time} s")