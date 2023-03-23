#!/usr/bin/env python3
# make_samIII_histograms.py
# Hunter Barndt
# Purpose: To plot SAM-III histogram data from pickled databases into a: multi year analysis, one year analysis, one day analysis? 

import plotly as plt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
import glob as gb
import time as tm
#pd.options.plotting.backend = "plotly"

### Global Variables
#start_year = 2009
start_year = 2010
end_year = 2022
num_years = end_year - start_year
all_samIII_years = []
all_gima_years = []

analysis_types = [
    "year_analysis-by_month-reading_count",
    "month_anaylsis-by_day-reading_count",
    "multiyear_analysis-by_year-reading_count",
    "multiyear_analysis-by_year-day_count"
]

analysis_types_abbrev = [
    "yabmrc",
    "mabdrc",
    "myabyrc",
    "myabydc"
]

### Prompts
print(f"Which year would you like to process? [Option(s): {start_year} thru {end_year}]")
while True:
    selected_year = input()
    if int(selected_year) >= (start_year + 1) or int(selected_year) <= end_year - 2:
        selected_year = int(selected_year)
        break
    else:
        print("Enter valid year.")

print(f"Process for each component or for x, y, and z or horizonal magnitude (H)? [Option(s): 'xyz' or 'H']")
while True:
    process_type = input()
    if process_type == 'xyz' or process_type == 'H':
        if process_type == 'xyz':
            components = ['x', 'y', 'z']
        else:
            components = ['H']
        break
    else:
        print("Enter process type.")
        
print(f"Which anaylsis would you like to make? ")
print(f"Option(s): ")
for i in range(len(analysis_types)):
    print(f"{analysis_types[i]} [Type ->: {analysis_types_abbrev[i]}]" )
while True:
    analysis_abbrev = input()
    if analysis_abbrev in analysis_types_abbrev:
        analysis = analysis_types[analysis_types_abbrev.index(analysis_abbrev)]
        break
    else:
        print("Enter valid year.")

### Load Datasets
# Load SAMIII Data
samIII_database_dir = f"D:/UAF/PHYS Capstone/pickles/samIII/*-SAMIII-Processed-Data.pickle"
samIII_database_dir_list = gb.glob(samIII_database_dir)
for database in samIII_database_dir_list:
    samIII_year_dataframe = pd.read_pickle(database)
    all_samIII_years.append(samIII_year_dataframe)
samIII_selected_year_path = f"D:/UAF/PHYS Capstone/pickles/samIII/{selected_year}-SAMIII-Processed-Data.pickle"
print("Created all_samII_years list...")

# Load GIMA Data
gima_database_dir = f"D:/UAF/PHYS Capstone/pickles/gima/*-GIMA-Processed-Data.pickle"
gima_database_dir_list = gb.glob(gima_database_dir)
for database in gima_database_dir_list:
    gima_year_dataframe = pd.read_pickle(database)
    all_gima_years.append(gima_year_dataframe)
gima_selected_year_path = f"D:/UAF/PHYS Capstone/pickles/gima/{selected_year}-GIMA-Processed-Data.pickle"
print("Created all_gima_years list...")

dateformat = "%d.%m.%Y %H:%M:%S"

### Functions
# Polymorphic analysis function
def run_analysis(selected_year_dataframe, all_samIII_years, all_gima_years, chosen_anaylsis):
    
    print("Starting function...")
    # Define all year dataframes
    #samIII_all_years_dataframe = pd.DataFrame()
    samIII_all_years_dataframe_max_day = pd.DataFrame()
    #gima_all_years_dataframe = pd.DataFrame()
    gima_all_years_dataframe_max_day = pd.DataFrame()
    
    print("Starting appendation...")
    # Append all years to dataframes
    for i, database in enumerate(all_samIII_years):
        temp_database = database
        temp_database['day'] = temp_database.datetime.dt.day
        temp_database = temp_database.groupby(['day']).max()
        samIII_all_years_dataframe_max_day = pd.concat([samIII_all_years_dataframe_max_day, temp_database])
        print(f"Calculated and added max day SAMIII dataframe: {i}")
        #samIII_all_years_dataframe = pd.concat([samIII_all_years_dataframe, database])
    #print(samIII_all_years_dataframe)
    del all_samIII_years
    
    for i, database in enumerate(all_gima_years):
        temp_database = database
        temp_database['day'] = temp_database.datetime.dt.day
        temp_database = temp_database.groupby(['day']).max()
        gima_all_years_dataframe_max_day = pd.concat([gima_all_years_dataframe_max_day, temp_database])
        print(f"Calculated and added max day GIMA dataframe: {i}")
        #gima_all_years_dataframe = pd.concat([gima_all_years_dataframe, database])
    #print(gima_all_years_dataframe)
    del all_gima_years
    
    print("Done with appending")
    # Define Thresholds
    day_threshold = 500
    month_threshold = 500
    year_threshold = 500
    
    # Number of days by year analysis 
    #selected_year_dataframe['month'] = selected_year_dataframe.datetime.dt.month
    #selected_year_dataframe['day'] = selected_year_dataframe.datetime.dt.day
    #samIII_all_years_dataframe['year'] = samIII_all_years_dataframe.datetime.dt.year
    samIII_all_years_dataframe_max_day['year'] = samIII_all_years_dataframe_max_day.datetime.dt.year
    #samIII_all_years_dataframe['day'] = samIII_all_years_dataframe.datetime.dt.day
    #selected_year_dataframe = selected_year_dataframe.drop(columns=['datetime'])
    #samIII_all_years_dataframe = samIII_all_years_dataframe.drop(columns=['datetime'])

    # Reading count by month for a year analysis
    if chosen_anaylsis == analysis_types[0]:
        selected_year_dataframe = selected_year_dataframe.drop(columns=['day'])
        selected_year_dataframe = selected_year_dataframe.set_index('month')

        for i in range(len(components)):
            fig1, ax1 = plt.subplots(figsize=[12,8])
            
            # Calculations
            one_comp_of_selected_year_dataframe = selected_year_dataframe[ (selected_year_dataframe[components[i]] > month_threshold) | (selected_year_dataframe[components[i]] < -month_threshold) ]
            if one_comp_of_selected_year_dataframe.empty:
                print(f"No valid values for {components[i]}-component calculations!!")
                continue
            one_comp_of_selected_year_dataframe_count_by_month = one_comp_of_selected_year_dataframe.groupby(['month']).count()
            one_comp_of_selected_year_dataframe_count_by_month = one_comp_of_selected_year_dataframe_count_by_month.reset_index()
            
            # Plotting month count plots
            one_comp_of_selected_year_dataframe_count_by_month.plot.bar(x='month', y=components[i])
            plt.title(f"SAM-III Magnetometer Data - Year {selected_year} - Counts of {components[i]}-component values > {month_threshold}")
            plt.savefig(f"./plots/histograms/{chosen_anaylsis}/{selected_year}/{month_threshold}/{selected_year}_{components[i]}-component_month_count_above_threshold_of_{month_threshold}.png")  
      
    # Reading count in days by month analysis   
    if chosen_anaylsis == analysis_types[1]:
        selected_year_dataframe = selected_year_dataframe.set_index('month')
        for month in selected_year_dataframe.index.unique():
            dataframe_of_month = selected_year_dataframe[ selected_year_dataframe.index == month ]

            for i in range(len(components)):
                fig1, ax1 = plt.subplots(figsize=[12,8])
                
                # Calculations
                one_comp_of_dataframe_of_month = dataframe_of_month[ (dataframe_of_month[components[i]] > day_threshold) | (dataframe_of_month[components[i]] < -day_threshold) ]
                if one_comp_of_dataframe_of_month.empty:
                    print(f"No valid values for {components[i]}-component calculations for the month: {month}!!")
                    continue
                one_comp_of_selected_year_dataframe_day_count_by_month = one_comp_of_dataframe_of_month.groupby(['day']).count()
                one_comp_of_selected_year_dataframe_day_count_by_month = one_comp_of_selected_year_dataframe_day_count_by_month.reset_index()
                
                # Plotting month count plots
                one_comp_of_selected_year_dataframe_day_count_by_month.plot.bar(x='day', y=components[i])
                plt.title(f"SAM-III Magnetometer Data - Year {selected_year} - Counts of {components[i]}-component values > {day_threshold}")
                plt.savefig(f"./plots/histograms/{chosen_anaylsis}/{selected_year}/{day_threshold}/{selected_year}_{month}_{components[i]}-component_day_count_above_threshold_of_{day_threshold}.png")
    
    # Reading count in year by years analysis    
    if chosen_anaylsis == analysis_types[2]:
        print("All years dataframe: ")
        print(all_years_dataframe)
        all_years_dataframe = all_years_dataframe.set_index('year')

        for i in range(len(components)):
            fig1, ax1 = plt.subplots(figsize=[12,8])
            
            # Calculations
            one_comp_of_all_years_dataframe = all_years_dataframe[ (all_years_dataframe[components[i]] > year_threshold) | (all_years_dataframe[components[i]] < -year_threshold) ]
            if one_comp_of_all_years_dataframe.empty:
                print(f"No valid values for {components[i]}-component calculations!!")
                continue

            one_comp_of_all_years_dataframe_count_by_month = one_comp_of_all_years_dataframe.groupby(['year']).count()
            one_comp_of_all_years_dataframe_count_by_month = one_comp_of_all_years_dataframe_count_by_month.reset_index()
            
            # Plotting month count plots
            one_comp_of_all_years_dataframe_count_by_month.plot.bar(x='year', y=components[i])
            plt.title(f"SAM-III Magnetometer Data - Counts of {components[i]}-component values > {year_threshold}")
            plt.savefig(f"./plots/histograms/{chosen_anaylsis}/{components[i]}-component_year_count_above_threshold_of_{year_threshold}.png")
    
    # Reading count in year by years analysis    
    if chosen_anaylsis == analysis_types[3]:
        
        samIII_all_years_dataframe_max_day = samIII_all_years_dataframe_max_day.set_index('year')
        #gima_all_years_dataframe_max_day = gima_all_years_dataframe_max_day.set_index('year')

        for i in range(len(components)):
            fig1, ax1 = plt.subplots(figsize=[12,8])
            
            # Calculations
            samIII_one_comp_of_all_years_dataframe = samIII_all_years_dataframe_max_day[ (samIII_all_years_dataframe_max_day[components[i]] > year_threshold) | (samIII_all_years_dataframe_max_day[components[i]] < -year_threshold) ]
            #gima_one_comp_of_all_years_dataframe = gima_all_years_dataframe_max_day[ (gima_all_years_dataframe_max_day[components[i]] > year_threshold) | (gima_all_years_dataframe_max_day[components[i]] < -year_threshold) ]
            if samIII_one_comp_of_all_years_dataframe.empty:
                print(f"No valid values for {components[i]}-component calculations!!")
                continue
            
            # Check and print data
            #print(samIII_one_comp_of_all_years_dataframe)
            samIII_one_comp_of_all_years_dataframe_count_by_month = samIII_one_comp_of_all_years_dataframe.groupby(['year']).count()
            #print(samIII_one_comp_of_all_years_dataframe_count_by_month)
            samIII_one_comp_of_all_years_dataframe_count_by_month = samIII_one_comp_of_all_years_dataframe_count_by_month.reset_index()
            print(f"Done with SAMIII: {i}")
            #print(gima_one_comp_of_all_years_dataframe)
            #gima_one_comp_of_all_years_dataframe_count_by_month = gima_one_comp_of_all_years_dataframe.groupby(['year']).count()
            #print(gima_one_comp_of_all_years_dataframe_count_by_month)
            #gima_one_comp_of_all_years_dataframe_count_by_month = gima_one_comp_of_all_years_dataframe_count_by_month.reset_index()
            print(f"Done with GIMA: {i}")
            
            # Plotting month count plots
            samIII_one_comp_of_all_years_dataframe_count_by_month.plot.bar(x='year', y=components[i])
            #gima_one_comp_of_all_years_dataframe_count_by_month.plot.bar(x='year', y=components[i])
            plt.title(f"SAM-III Magnetometer Data - Counts of {components[i]}-component values > {year_threshold}")
            plt.savefig(f"./plots/histograms/{chosen_anaylsis}/{components[i]}-component_year_count_above_threshold_of_{year_threshold}.png")

### Main
def main():

    samIII_selected_year_dataframe = pd.read_pickle(samIII_selected_year_path)

    run_analysis(selected_year_dataframe=samIII_selected_year_dataframe, all_samIII_years=all_samIII_years, all_gima_years=all_gima_years, chosen_anaylsis=analysis)

start_time = tm.time()
main()
end_time = tm.time()
print(f"Time to Excecute: {end_time-start_time} s")

