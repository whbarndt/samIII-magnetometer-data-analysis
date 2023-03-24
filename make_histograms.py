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
    "month_analysis-by_day-reading_count",
    "multiyear_analysis-by_year-reading_count",
    "multiyear_analysis-by_year-resampled_count"
]

analysis_types_abbrev = [
    "yabmrc",
    "mabdrc",
    "myabyrc",
    "myabyrspc"
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
        print("Enter valid analysis.")

print("\n")
print("\n")
print("### Next prompts only apply to analysis: \"multiyear_analysis-by_year-resampled_count\" ###")
print("\n")
print("\n")   
print(f"Would you like to resample, and with what frequency of the data? [Options: T (minute), D (daily), W (weekly), M (monthly)]")
while True:
    resample = input()
    if resample in [None, 'T', 'D', 'W', 'M']:
        break
    else:
        print("Enter valid resample rate.")

'''
Unused. Yet.
print(f"Which function would you like to use with the resample? [Options: max, min, mean]")
while True:
    resample_function = input()
    if resample_function in ['max', 'min', 'mean']:
        break
    else:
        print("Enter valid resample function.")'''

dateformat = "%d.%m.%Y %H:%M:%S"

### Functions
# Polymorphic analysis function
def run_analysis(samIII_selected_year_dataframe, gima_selected_year_dataframe, gima_all_years_dataframe, samIII_all_years_dataframe, chosen_anaylsis, resample):
    
    print("Starting analysis function...")
    
    # Define Thresholds
    day_threshold = 500
    month_threshold = 500
    year_threshold = 500

    # Number of readings above threshold by each month, for a year - "year_analysis-by_month-reading_count"
    if chosen_anaylsis == analysis_types[0]:
        print(f"Month Threshold: {month_threshold}")
        for i in range(len(components)):
            fig1, ax1 = plt.subplots(figsize=[12,8])
            # Calculations
            one_comp_of_samIII_selected_year_dataframe = samIII_selected_year_dataframe[ (samIII_selected_year_dataframe[components[i]] > month_threshold) | (samIII_selected_year_dataframe[components[i]] < -month_threshold) ]
            if one_comp_of_samIII_selected_year_dataframe.empty:
                print(f"No valid values for {components[i]}-component calculations!!")
                continue
            
            one_comp_of_samIII_selected_year_dataframe_count_by_month = one_comp_of_samIII_selected_year_dataframe.resample('M').count()
            one_comp_of_samIII_selected_year_dataframe_count_by_month['month'] = one_comp_of_samIII_selected_year_dataframe_count_by_month.index.month
            
            # Plotting month count plots
            one_comp_of_samIII_selected_year_dataframe_count_by_month.plot.bar(x='month', y=components[i])
            plt.title(f"SAM-III Magnetometer Data - Year {selected_year} - Reading counts of {components[i]}-component values > {month_threshold} nT")
            plt.savefig(f"./plots/histograms/{chosen_anaylsis}/{selected_year}/{month_threshold}/{selected_year}_{components[i]}-component_month_reading_count_above_threshold_of_{month_threshold}.png")  
      
    # Number of readings above threshold by each day, for each month, for a year - "month_analysis-by_day-reading_count"
    if chosen_anaylsis == analysis_types[1]:
        print(f"Day Threshold: {day_threshold}")
        for month in samIII_selected_year_dataframe.index.month.unique():
            dataframe_of_month = samIII_selected_year_dataframe[ samIII_selected_year_dataframe.index.month == month ]

            for i in range(len(components)):
                fig1, ax1 = plt.subplots(figsize=[12,8])
                
                # Calculations
                one_comp_of_samIII_selected_year_dataframe = dataframe_of_month[ (dataframe_of_month[components[i]] > day_threshold) | (dataframe_of_month[components[i]] < -day_threshold) ]
                if one_comp_of_samIII_selected_year_dataframe.empty:
                    print(f"No valid values for {components[i]}-component calculations for the month: {month}!!")
                    continue
                
                one_comp_of_samIII_selected_year_dataframe_count_by_month = one_comp_of_samIII_selected_year_dataframe.resample('D').count()
                one_comp_of_samIII_selected_year_dataframe_count_by_month['day'] = one_comp_of_samIII_selected_year_dataframe_count_by_month.index.day
                
                # Plotting month count plots
                one_comp_of_samIII_selected_year_dataframe_count_by_month.plot.bar(x='day', y=components[i])
                plt.title(f"SAM-III Magnetometer Data - Year {selected_year} - Reading counts of {components[i]}-component values > {day_threshold} nT")
                plt.savefig(f"./plots/histograms/{chosen_anaylsis}/{selected_year}/{day_threshold}/{selected_year}_{month}_{components[i]}-component_day_reading_count_above_threshold_of_{day_threshold}.png")
    
    # Number of readings above threshold by each year, for multiple years - "multiyear_analysis-by_year-reading_count",
    if chosen_anaylsis == analysis_types[2]:
        print("All years dataframe: ")
        print(samIII_all_years_dataframe)

        for i in range(len(components)):
            fig1, ax1 = plt.subplots(figsize=[12,8])
            
            # Calculations
            one_comp_of_all_years_dataframe = samIII_all_years_dataframe[ (samIII_all_years_dataframe[components[i]] > year_threshold) | (samIII_all_years_dataframe[components[i]] < -year_threshold) ]
            if one_comp_of_all_years_dataframe.empty:
                print(f"No valid values for {components[i]}-component calculations!!")
                continue

            one_comp_of_all_years_dataframe_count_by_month = one_comp_of_all_years_dataframe.resample('A').count()
            one_comp_of_all_years_dataframe_count_by_month['year'] = one_comp_of_all_years_dataframe_count_by_month.index.year
            
            # Plotting month count plots
            one_comp_of_all_years_dataframe_count_by_month.plot.bar(x='year', y=components[i])
            plt.title(f"SAM-III Magnetometer Data - Reading counts of {components[i]}-component values > {year_threshold} nT")
            plt.savefig(f"./plots/histograms/{chosen_anaylsis}/{components[i]}-component_year_count_above_threshold_of_{year_threshold}.png")
    
    # Number of days above threshold by each year, for multiple years - "multiyear_analysis-by_year-day_count",
    if chosen_anaylsis == analysis_types[3]:
        for i in range(len(components)):
            
            # Calculations
            samIII_one_comp_of_all_years_dataframe = samIII_all_years_dataframe[ (samIII_all_years_dataframe[components[i]] > year_threshold) | (samIII_all_years_dataframe[components[i]] < -year_threshold) ]
            gima_one_comp_of_all_years_dataframe = gima_all_years_dataframe[ (gima_all_years_dataframe[components[i]] > year_threshold) | (gima_all_years_dataframe[components[i]] < -year_threshold) ]
            if samIII_one_comp_of_all_years_dataframe.empty:
                print(f"No valid values for {components[i]}-component calculations!!")
                continue
            
            # Check, print, and resample data
            print(f"Starting the resampling for {components[i]}")
            samIII_one_comp_of_all_years_dataframe_resampled_count = samIII_one_comp_of_all_years_dataframe.resample(resample).max().resample("Y").count()
            samIII_one_comp_of_all_years_dataframe_resampled_count['year'] = samIII_one_comp_of_all_years_dataframe_resampled_count.index.year
            print(f"Done with SAMIII: {components[i]}")
            gima_one_comp_of_all_years_dataframe_resampled_count = gima_one_comp_of_all_years_dataframe.resample(resample).max().resample("Y").count()
            gima_one_comp_of_all_years_dataframe_resampled_count['year'] = gima_one_comp_of_all_years_dataframe_resampled_count.index.year
            print(f"Done with GIMA: {components[i]}")
            print(f"Resampled Dataframes of dim {components[i]}:")
            #print(samIII_one_comp_of_all_years_dataframe_resampled_count)
            #print(gima_one_comp_of_all_years_dataframe_resampled_count)
            
            # Plotting month count plots
            
            # Width of a bar 
            width = 0.3       

            # Plotting
            fig1, ax1 = plt.subplots(figsize=[12,8])
            ax1.bar(samIII_one_comp_of_all_years_dataframe_resampled_count.year.tolist(), samIII_one_comp_of_all_years_dataframe_resampled_count[components[i]].tolist(), width, label='SAMIII')
            ax1.bar(list(np.asarray(gima_one_comp_of_all_years_dataframe_resampled_count.year.tolist()) + width), gima_one_comp_of_all_years_dataframe_resampled_count[components[i]].tolist(), width, label='GIMA')
            # Finding the best position for legends and putting it
            #samIII_one_comp_of_all_years_dataframe_resampled_count.plot.bar(ax=ax1, x='year', y=components[i], color='red')
            #gima_one_comp_of_all_years_dataframe_resampled_count.plot.bar(ax=ax1, x='year', y=components[i], color='blue')
            plt.title(f"GIMA and SAMIII Magnetometer Data - {resample} counts of {components[i]}-component values > {year_threshold} nT")
            plt.legend(loc='best')
            plt.xlabel('Year')
            plt.ylabel('# of Days')
            # First argument - A list of positions at which ticks should be placed
            # Second argument -  A list of labels to place at the given locations
            plt.xticks(list(np.asarray(samIII_one_comp_of_all_years_dataframe_resampled_count.year.tolist()) + width / 2), samIII_one_comp_of_all_years_dataframe_resampled_count.year.tolist())
            plt.savefig(f"./plots/histograms/{chosen_anaylsis}/{components[i]}-component_year_{resample}_count_above_threshold_of_{year_threshold}.png")

### Main
def main():
    
    ### Load Datasets
    
    # Define all year dataframes
    samIII_all_years_dataframe = pd.DataFrame()
    gima_all_years_dataframe = pd.DataFrame()
    
    # Load SAMIII Data
    samIII_database_dir = f"D:/UAF/PHYS Capstone/pickles/samIII/*-SAMIII-Processed-Data.pickle"
    samIII_multiyear_database_dir = f"D:/UAF/PHYS Capstone/pickles/samIII/{start_year}-{end_year}-SAMIII-Processed-Data.pickle"
    samIII_selected_year_path = f"D:/UAF/PHYS Capstone/pickles/samIII/{selected_year}-SAMIII-Processed-Data.pickle"
    samIII_database_dir_list = gb.glob(samIII_database_dir)
    
    try:
        samIII_all_years_dataframe = pd.read_pickle(samIII_multiyear_database_dir)
        print(f"{samIII_multiyear_database_dir} read successfully!")
    except:
        for database in samIII_database_dir_list:
            samIII_year_dataframe = pd.read_pickle(database)
            samIII_year_dataframe = samIII_year_dataframe.set_index('datetime')
            samIII_all_years_dataframe = pd.concat([samIII_all_years_dataframe, database])
            print(f"Appended SAMIII year dataframe: {start_year + i}")
        samIII_all_years_dataframe.to_pickle(samIII_multiyear_database_dir)

    samIII_selected_year_dataframe = pd.read_pickle(samIII_selected_year_path)
    samIII_selected_year_dataframe = samIII_selected_year_dataframe.set_index('datetime')

    # Load GIMA Data
    gima_database_dir = f"D:/UAF/PHYS Capstone/pickles/gima/*-GIMA-Processed-Data.pickle"
    gima_multiyear_database_dir = f"D:/UAF/PHYS Capstone/pickles/gima/{start_year}-{end_year}-GIMA-Processed-Data.pickle"
    gima_selected_year_path = f"D:/UAF/PHYS Capstone/pickles/gima/{selected_year}-GIMA-Processed-Data.pickle"
    gima_database_dir_list = gb.glob(gima_database_dir)
    
    try:
        gima_all_years_dataframe = pd.read_pickle(gima_multiyear_database_dir)
        print(f"{gima_multiyear_database_dir} read successfully!")
    except:
        for database in gima_database_dir_list:
            gima_year_dataframe = pd.read_pickle(database)
            gima_year_dataframe = gima_year_dataframe.set_index('datetime')
            gima_all_years_dataframe = pd.concat([gima_all_years_dataframe, database])
            print(f"Appended GIMA year dataframe: {start_year + i}")
        gima_all_years_dataframe.to_pickle(gima_multiyear_database_dir)
    
    gima_selected_year_dataframe = pd.read_pickle(gima_selected_year_path)
    gima_selected_year_dataframe = gima_selected_year_dataframe.set_index('datetime')

    run_analysis(samIII_selected_year_dataframe=samIII_selected_year_dataframe, gima_selected_year_dataframe=gima_selected_year_dataframe, samIII_all_years_dataframe=samIII_all_years_dataframe, gima_all_years_dataframe=gima_all_years_dataframe, chosen_anaylsis=analysis, resample=resample)

start_time = tm.time()
main()
end_time = tm.time()
print(f"Time to Excecute: {end_time-start_time} s")

