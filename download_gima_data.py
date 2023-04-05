#!/usr/bin/env python3
# Hunter Barndt
# download_gima_data.py
# Purpose: Download GIMA data from: http://magnetometer.rcs.alaska.edu/DATA/www

### CAN BE GENERALIZED TO RCS MAG WEBSITES (e.g. swugatlas)

import wget

# Self created imports
from define import gima_sites
from define import gima_website
from define import num_months
from define import num_days
from define import download_start_year
from define import download_end_year

'''# Select the year for which to download the files
print(f"Which year would you like to download? [Option(s): {start_year} thru {end_year}]")
while True:
    year = input()
    if int(year) >= (start_year) or int(year) <= end_year:
        year = int(year)
        break
    else:
        print("Enter valid year.")'''

# Loop over all possible combinations of month, day, and location
for year in range(download_start_year, download_end_year + 1):
    for month in range(1, num_months + 1):
        for day in range(1, num_days + 1):
            for location in gima_sites:
                # Construct the URL for the CSV file
                url = f'{gima_website}/DATA/www/{year}/{month:02d}/{day:02d}/{location}/{location}_{year}_{month:02d}_{day:02d}.csv'
                
                try:
                    # Download the CSV file using wget
                    filename = wget.download(url)
                    # Print a message indicating the download was successful
                    
                    print(f" CSV file downloaded to {filename}")
                except:
                    # If the download fails, print an error message
                    print(f" Error downloading {url}")
