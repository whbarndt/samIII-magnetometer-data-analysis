#!/usr/bin/env python3
# samIII_data_parser.py
# Hunter Barndt
# Purpose: To parse SAM-III data from text files

import glob as gb
import pandas as pd
import time as tm

# Self created imports
from define import *

### Global Variables ###

print(f"Which data source would you like to process from? [Option(s): \'swugatlas\' or \'reeves\']")
while True:
    data_source = input()
    if data_source == 'swugatlas' or data_source == 'reeves':
        break
    else:
        print("Enter valid year.")

print(f"Which year would you like to process? [Option(s): Reeves: {reeves_start_year} thru {reeves_end_year} | SWUGAtlas: {swugat_start_year} thru {swugat_end_year}]")
while True:
    selected_year = input()
    if data_source == 'reeves':
        if int(selected_year) >= (reeves_start_year + 1) or int(selected_year) <= reeves_end_year - 2:
            #if int(selected_year) == 2009:
            #    srcdir = f'{directory_preambles[current_machine]}Reeve_Anchorage_SAM_Data/{selected_year}/*.txt'
            if int(selected_year) == 2010:
                srcdir = f'{directory_preambles[current_machine]}Reeve_Anchorage_SAM_Data/{selected_year}/SAM-III/*.txt'
            elif int(selected_year) >= 2011 and int(selected_year) <= 2014:
                srcdir = f'{directory_preambles[current_machine]}Reeve_Anchorage_SAM_Data/{selected_year}/*.txt'
            elif int(selected_year) >= 2015 and int(selected_year) <= 2016:
                srcdir = f'{directory_preambles[current_machine]}Reeve_Anchorage_SAM_Data/{selected_year}/Logs-Text Files/*.txt'
            elif int(selected_year) >= 2017 and int(selected_year) <= 2019:
                srcdir = f'{directory_preambles[current_machine]}Reeve_Anchorage_SAM_Data/{selected_year}/Text-Log Files/*.txt'
            elif int(selected_year) == 2020:
                srcdir = f'{directory_preambles[current_machine]}Reeve_Anchorage_SAM_Data/{selected_year}/Archive .log .txt/*.txt'
            elif int(selected_year) == 2021:
                srcdir = f'{directory_preambles[current_machine]}Reeve_Anchorage_SAM_Data/{selected_year}/Txt Log Files/*.txt'
            elif int(selected_year) == 2022:
                srcdir = f'{directory_preambles[current_machine]}Reeve_Anchorage_SAM_Data/{selected_year}/Daily Txt Log Files .txt .log/*.txt'
            else:
                print("Please select another year.")
            break
    if data_source == 'swugatlas':
        if int(selected_year) >= (swugat_start_year + 1) or int(selected_year) <= swugat_end_year - 2:
            if int(selected_year) == 2023:
                srcdir = f'{directory_preambles[current_machine]}swugatlas_SAM_Data/{swugat_site}/{selected_year}/*.csv'
    else:
        print("Enter valid year.")


data_files_paths = gb.glob(srcdir)
data_files_paths.sort()

# Creating Erroneous data files to looking at the data closer
fullgreaterthan_file_path = f'{directory_preambles[current_machine]}error/fullgreaterthan3_{selected_year}.txt'
fullgreaterthan_file = open(fullgreaterthan_file_path, 'w')
fulllessthan_file_path = f'{directory_preambles[current_machine]}error/fulllessthan3_{selected_year}.txt'
fulllessthan_file = open(fulllessthan_file_path, 'w')
datagreaterthan_file_path = f'{directory_preambles[current_machine]}error/datagreaterthan6_{selected_year}.txt'
datagreaterthan_file = open(datagreaterthan_file_path, 'w')
datalessthan_file_path = f'{directory_preambles[current_machine]}error/datalessthan6_{selected_year}.txt'
datalessthan_file = open(datalessthan_file_path, 'w')
datetime_nottwo_file_path = f'{directory_preambles[current_machine]}error/datatime_nottwo_{selected_year}.txt'
datetime_nottwo_file = open(datetime_nottwo_file_path, 'w')

pickle_path_name = f"{directory_preambles[current_machine]}pickles/{selected_year}-SAMIII-{data_source}-Data.pickle"
csv_path_name = f"{directory_preambles[current_machine]}csvs/{selected_year}-SAMIII-{data_source}-Data.csv"

datetimeformat = "%d.%m.%y %H:%M:%S"

dim = ['x', 'y', 'z']
datetime_array = []
x_array = []
y_array = []
z_array = []

### Functions ###

# Input:    line from a file, the storage arrays for the datetime, x-component, y-component, and the z-component 
# Output:   Null, just appends to storage arrays
def parse_reeves_line(line, datetime, x, y, z):
    #print(line)
    date_coord_split = line.split(" ")
    # If full line structure has some errors
    if len(date_coord_split) != 3:
        if len(date_coord_split) > 3:
            fullgreaterthan_file.write(f'{line}\n')
            #date_coord_split = [date_coord_split[0], date_coord_split[1][0:8], date_coord_split[-1]]
        if len(date_coord_split) < 3:
            fulllessthan_file.write(f'{line}\n')
    elif len(date_coord_split) == 3:
        coord_split = date_coord_split[-1].split(',')
        # If the datetime format has errors
        datesplit = date_coord_split[0].split(".")
        timesplit = date_coord_split[1][0:8].split(":")
        for i in range(len(datesplit)):
            if len(datesplit[i]) != 2 or len(timesplit[i]) != 2:
                datetime_nottwo_file.write(f'{line}\n')
        # If the x,y,z data structure has errors
        if (len(coord_split) < 6):
            datalessthan_file.write(f'{line}\n')
        elif (len(coord_split) > 6):
            datagreaterthan_file.write(f'{line}\n')
        # Good otherwise
        else:
            datetime.append(f"{date_coord_split[0]} {date_coord_split[1][0:8]}")
            x.append(coord_split[1])
            y.append(coord_split[3])
            z.append(coord_split[5].replace("\n",""))

# Input:    line from a file, the storage arrays for the datetime, x-component, y-component, and the z-component 
# Output:   Null, just appends to storage arrays
def parse_swugat_line(line, datetime, x, y, z):
    #print(line)
    date_coord_split = line.split(" ")
    # If full line structure has some errors
    if len(date_coord_split) != 3:
        if len(date_coord_split) > 3:
            fullgreaterthan_file.write(f'{line}\n')
            #date_coord_split = [date_coord_split[0], date_coord_split[1][0:8], date_coord_split[-1]]
        if len(date_coord_split) < 3:
            fulllessthan_file.write(f'{line}\n')
    elif len(date_coord_split) == 3:
        coord_split = date_coord_split[-1].split(',')
        # If the datetime format has errors
        datesplit = date_coord_split[0].split(".")
        timesplit = date_coord_split[1][0:8].split(":")
        for i in range(len(datesplit)):
            if len(datesplit[i]) != 2 or len(timesplit[i]) != 2:
                datetime_nottwo_file.write(f'{line}\n')
        # If the x,y,z data structure has errors
        if (len(coord_split) < 6):
            datalessthan_file.write(f'{line}\n')
        elif (len(coord_split) > 6):
            datagreaterthan_file.write(f'{line}\n')
        # Good otherwise
        else:
            datetime.append(f"{date_coord_split[0]} {date_coord_split[1][0:8]}")
            x.append(coord_split[1])
            y.append(coord_split[3])
            z.append(coord_split[5].replace("\n",""))

# Input:    Dataframe
# Output:   Same dataframe except with the int type in the x,y,z component columns and datetime type for datetime column 
def set_dataframe_types(df):
    for i in dim:
        df[i] = df[i].astype(int)
    df['datetime'] = pd.to_datetime(df['datetime'], format=datetimeformat)
    return df

### Main ###
def main():
    for path in data_files_paths:
        file = open(path)
        for line in file:
            parse_reeves_line(line, datetime_array, x_array, y_array, z_array)
        file.close()
    data_dict = {
        'datetime': datetime_array,
        'x': x_array,
        'y': y_array,
        'z': z_array,
    }
    dataframe = pd.DataFrame(data_dict)
    dataframe = set_dataframe_types(dataframe)
    dataframe = dataframe.set_index('datetime')
    dataframe = dataframe.sort_index()
    dataframe.to_pickle(pickle_path_name)
    dataframe.to_csv(csv_path_name)

start_time = tm.time()
main()
end_time = tm.time()
print(f"Time to Excecute: {end_time-start_time} s")

# Close erroneous data files
fullgreaterthan_file.close()
fulllessthan_file.close()
datagreaterthan_file.close()
datalessthan_file.close()
datetime_nottwo_file.close()