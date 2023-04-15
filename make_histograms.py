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

# Self created imports
from define import gima_sites
from define import gima_site 
from define import current_machine
from define import directory_preambles

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
    "multiyear_analysis-by_year-resampled_count",
    "multiyear_analysis-by_year-resampled_dhdt_count"
]

analysis_types_abbrev = [
    "yabmrc",
    "mabdrc",
    "myabyrc",
    "myabyrspc",
    "myabyrspdc"
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
            components = ['x','y','z']
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
print("###") 
print("Next prompts only apply to analysis: ")
for i in range(2):
    print(f"{analysis_types[i+3]}" )
print("###")
print("\n")   

print(f"Would you like to resample, and with what frequency of the data? [Options: T (minute), D (daily), W (weekly), M (monthly)]")
while True:
    resample = input()
    if resample in [None, 'T', 'D', 'W', 'M']:
        break
    else:
        print("Enter valid resample rate.")

print(f"Would you like to include Sun Spot Totals in the graphs? [Options: yes, no]")
while True:
    sun_spot_flag_input = input()
    if sun_spot_flag_input == 'yes':
        sunspot_flag = True
        break
    elif sun_spot_flag_input == 'no':
        sunspot_flag = False
        break
    else:
        print("Enter valid answer.")

print(f"Would you like to plot in log-scale? [Options: yes, no]")
while True:
    logscale_flag_input = input()
    if logscale_flag_input == 'yes':
        logscale_flag = True
        break
    elif logscale_flag_input == 'no':
        logscale_flag = False
        break
    else:
        print("Enter valid answer.")

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
def run_analysis(samIII_selected_year_dataframe, gima_selected_year_dataframe, samIII_all_years_dataframe, samIII_multiyear_database_dir, gima_all_years_dataframe, gima_multiyear_database_dir, chosen_anaylsis, resample):
    
    print("Starting analysis function...")
    # Define Thresholds
    day_threshold = 500
    month_threshold = 500
    year_threshold = 500
    diff_threshold = 6

    fig_size=[15,10]

    # Number of readings above threshold by each month, for a year - "year_analysis-by_month-reading_count"
    if chosen_anaylsis == analysis_types[0]:
        print(f"Month Threshold: {month_threshold}")
        for i in range(len(components)):
            fig1, ax1 = plt.subplots(figsize=fig_size)
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
                fig1, ax1 = plt.subplots(figsize=fig_size)
                
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
            fig1, ax1 = plt.subplots(figsize=fig_size)
            
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
            
            # Print all years dataframes
            print(samIII_all_years_dataframe)
            print(gima_all_years_dataframe)
            
            # Filter based on threshold
            samIII_one_comp_of_all_years_dataframe = samIII_all_years_dataframe[ (samIII_all_years_dataframe[components[i]] > year_threshold) | (samIII_all_years_dataframe[components[i]] < -year_threshold) ]
            gima_one_comp_of_all_years_dataframe = gima_all_years_dataframe[ (gima_all_years_dataframe[components[i]] > year_threshold) | (gima_all_years_dataframe[components[i]] < -year_threshold) ]
            
            del samIII_all_years_dataframe
            del gima_all_years_dataframe
            
            if samIII_one_comp_of_all_years_dataframe.empty:
                print(f"No valid values for {components[i]}-component calculations!!")
                continue
            
            print(f"Starting the resampling for {components[i]}")
            try: 
                samIII_one_comp_of_all_years_dataframe = pd.read_pickle(f"{samIII_multiyear_database_dir[:-7]}_resampled_{resample}_{year_threshold}.pickle")
            except:
                samIII_one_comp_of_all_years_dataframe = samIII_one_comp_of_all_years_dataframe.resample(resample).max()
                samIII_one_comp_of_all_years_dataframe = samIII_one_comp_of_all_years_dataframe.resample("Y").count()
                #samIII_one_comp_of_all_years_dataframe = samIII_one_comp_of_all_years_dataframe.resample(resample).max().resample("Y").count()
                samIII_one_comp_of_all_years_dataframe.to_pickle(f"{samIII_multiyear_database_dir[:-7]}_resampled_{resample}_{year_threshold}.pickle")
            samIII_one_comp_of_all_years_dataframe['year'] = samIII_one_comp_of_all_years_dataframe.index.year
            
            print(f"Done with SAMIII: {components[i]}")
            try: 
                gima_one_comp_of_all_years_dataframe = pd.read_pickle(f"{gima_multiyear_database_dir[:-7]}_resampled_{resample}_{year_threshold}.pickle")
            except:
                gima_one_comp_of_all_years_dataframe = gima_one_comp_of_all_years_dataframe.resample(resample).max()
                gima_one_comp_of_all_years_dataframe = gima_one_comp_of_all_years_dataframe.resample("Y").count()
                #gima_one_comp_of_all_years_dataframe = gima_one_comp_of_all_years_dataframe.resample(resample).max().resample("Y").count()
                gima_one_comp_of_all_years_dataframe.to_pickle(f"{gima_multiyear_database_dir[:-7]}_resampled_{resample}_{year_threshold}.pickle")
            gima_one_comp_of_all_years_dataframe['year'] = gima_one_comp_of_all_years_dataframe.index.year
            print(f"Done with GIMA: {components[i]}")
            
            print(f"Resampled Dataframes of dim {components[i]}:")
        
            # Width of a bar 
            width = 0.3       

            # Plotting
            fig1, ax1 = plt.subplots(figsize=fig_size)
            # Sun Spot Data
            if sunspot_flag == True:
                # Loading Sunspot data
                ssn_df = pd.read_csv(f"{directory_preambles[current_machine]}SN_y_tot_V2.0.csv")
                ssn_df.Year = ssn_df.Year-0.5
                ax2 = ax1.twinx()
                ax2.plot(ssn_df.Year, ssn_df.Total)
                ax2.fill_between(np.arange(2008,2023,1), ssn_df.Total[ssn_df.Year>=2008], 0, color='green', alpha=0.4)
                ax2.set_ylabel('Sun Spot Total #')
                ax2.set_ylim(bottom=0)
            # Histogram Count Data
            ax1.bar(samIII_one_comp_of_all_years_dataframe.year.tolist(), samIII_one_comp_of_all_years_dataframe[components[i]].tolist(), width, label='SAMIII')
            ax1.bar(list(np.asarray(gima_one_comp_of_all_years_dataframe.year.tolist()) + width), gima_one_comp_of_all_years_dataframe[components[i]].tolist(), width, label='GIMA')
            # Finding the best position for legends and putting it
            ax1.legend(loc='best')
            ax1.set_xlabel('Year')
            ax1.set_ylabel('# of Days')
            # First argument - A list of positions at which ticks should be placed
            # Second argument -  A list of labels to place at the given locations
            plt.xticks(list(np.asarray(gima_one_comp_of_all_years_dataframe.year.tolist()) + width / 2), gima_one_comp_of_all_years_dataframe.year.tolist())
            plt.xlim([2009,2022])
            plt.title(f"GIMA and SAMIII Magnetometer Data - {resample} counts of {components[i]}-component values > {year_threshold} nT")
            plt.savefig(f"./plots/histograms/{chosen_anaylsis}/{components[i]}-component_year_{resample}_count_above_threshold_of_{year_threshold}.png")
    if chosen_anaylsis == analysis_types[4]:
        
        # Filter based on threshold
        samIII_all_years_dataframe = samIII_all_years_dataframe[ (samIII_all_years_dataframe['dbdt'] > diff_threshold) | (samIII_all_years_dataframe['dbdt'] < -diff_threshold) ]
        gima_all_years_dataframe = gima_all_years_dataframe[ (gima_all_years_dataframe['dbdt'] > diff_threshold) | (gima_all_years_dataframe['dbdt'] < -diff_threshold) ]
        
        # Convert all inf to nan and drop rows with them
        gima_all_years_dataframe.replace([np.inf, -np.inf], np.nan, inplace=True)
        gima_all_years_dataframe.dropna(inplace=True)
        
        print(samIII_all_years_dataframe)
        print(gima_all_years_dataframe)
        
        # Resample to get year count
        samIII_all_years_dataframe = samIII_all_years_dataframe.resample(resample).max()
        samIII_all_years_dataframe = samIII_all_years_dataframe.resample("Y").count()
        samIII_all_years_dataframe['year'] = samIII_all_years_dataframe.index.year
        gima_all_years_dataframe = gima_all_years_dataframe.resample(resample).max()
        gima_all_years_dataframe = gima_all_years_dataframe.resample("Y").count()
        gima_all_years_dataframe['year'] = gima_all_years_dataframe.index.year

        print(samIII_all_years_dataframe)
        print(gima_all_years_dataframe)

        # Width of a bar 
        width = 0.3       

        # Plotting
        fig1, ax1 = plt.subplots(figsize=fig_size)
        # Sun Spot Data
        if sunspot_flag == True:
            # Loading Sunspot data
            ssn_df = pd.read_csv(f"{directory_preambles[current_machine]}SN_y_tot_V2.0.csv")
            ssn_df.Year = ssn_df.Year-0.5
            ax2 = ax1.twinx()
            ax2.plot(ssn_df.Year, ssn_df.Total)
            ax2.fill_between(np.arange(2008,2023,1), ssn_df.Total[ssn_df.Year>=2008], 0, color='green', alpha=0.4)
            ax2.set_ylabel('Sun Spot Total #')
            ax2.set_ylim(bottom=0)
        # Histogram Count Data
        if logscale_flag == True:
            ax1.set_yscale('log')
        ax1.bar(samIII_all_years_dataframe.year.tolist(), samIII_all_years_dataframe['dbdt'].tolist(), width, label='SAMIII')
        ax1.bar(list(np.asarray(gima_all_years_dataframe.year.tolist()) + width), gima_all_years_dataframe['dbdt'].tolist(), width, label='GIMA')
        # Finding the best position for legends and putting it
        ax1.legend(loc='best')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('# of dH/dt counts')
        # First argument - A list of positions at which ticks should be placed
        # Second argument -  A list of labels to place at the given locations
        plt.xticks(list(np.asarray(gima_all_years_dataframe.year.tolist()) + width / 2), gima_all_years_dataframe.year.tolist())
        plt.xlim([2009,2022])
        plt.title(f"GIMA and SAMIII Magnetometer Data - minute counts of dH/dt values > {diff_threshold} nT/s")
        plt.savefig(f"./plots/histograms/{chosen_anaylsis}/dH-dt_year_{resample}_count_above_threshold_of_{diff_threshold}.png")
        
### Main
def main():
    
    ### Load Datasets
    
    # Define all year dataframes
    samIII_all_years_dataframe = pd.DataFrame()
    gima_all_years_dataframe = pd.DataFrame()
    
    # Load SAMIII Data
    samIII_database_dir = f"{directory_preambles[current_machine]}pickles/samIII/*-SAMIII-Processed-Data.pickle"
    #samIII_multiyear_database_dir = f"{directory_preambles[current_machine]}pickles/samIII/{start_year}-{end_year}-SAMIII-Processed-Data.pickle"
    samIII_multiyear_database_dir = f"{directory_preambles[current_machine]}pickles/samIII/samIII_{start_year}_to_{end_year}_1min.pkl"
    samIII_selected_year_path = f"{directory_preambles[current_machine]}pickles/samIII/{selected_year}-SAMIII-Processed-Data.pickle"
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
    #samIII_selected_year_dataframe = samIII_selected_year_dataframe.set_index('datetime')

    # Load GIMA Data
    gima_database_dir = f"{directory_preambles[current_machine]}pickles/gima/{gima_site}/*-GIMA-Processed-Data.pickle"
    #gima_multiyear_database_dir = f"{directory_preambles[current_machine]}pickles/gima/{gima_site}/{start_year}-{end_year}-GIMA-{gima_site}-Processed-Data.pickle"
    gima_multiyear_database_dir = f"{directory_preambles[current_machine]}pickles/gima/{gima_site}/gima_{start_year}_to_{end_year}_1min.pkl"
    gima_selected_year_path = f"{directory_preambles[current_machine]}pickles/gima/{gima_site}/{selected_year}-GIMA-{gima_site}-Processed-Data.pickle"
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
    #gima_selected_year_dataframe = gima_selected_year_dataframe.set_index('datetime')

    run_analysis(samIII_selected_year_dataframe=samIII_selected_year_dataframe, gima_selected_year_dataframe=gima_selected_year_dataframe, samIII_all_years_dataframe=samIII_all_years_dataframe, samIII_multiyear_database_dir=samIII_multiyear_database_dir, gima_all_years_dataframe=gima_all_years_dataframe, gima_multiyear_database_dir=gima_multiyear_database_dir, chosen_anaylsis=analysis, resample=resample)

start_time = tm.time()
main()
end_time = tm.time()
print(f"Time to Excecute: {end_time-start_time} s")