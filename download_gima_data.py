#!/usr/bin/env python3
# Hunter Barndt
# download_gima_data.py
# Purpose: Download GIMA data from: http://magnetometer.rcs.alaska.edu/DATA/www

import wget

# Self created imports
from define import gima_sites
from define import gima_website
from define import num_months
from define import num_days
from define import gima_download_start_year
from define import gima_download_end_year

# Loop over all possible combinations of month, day, and location
for year in range(gima_download_start_year, gima_download_end_year + 1):
    for month in range(1, num_months + 1):
        for day in range(1, num_days + 1):
            for location in gima_sites:
                # URL of site for a CSV file
                url = f'{gima_website}/DATA/www/{year}/{month:02d}/{day:02d}/{location}/{location}_{year}_{month:02d}_{day:02d}.csv'
                
                try:
                    # Download using wget
                    filename = wget.download(url)
                    # Indicating the download was successful
                    print(f" CSV file downloaded to {filename}")
                except:
                    # If not, print that it failed
                    print(f" Error downloading {url}")
