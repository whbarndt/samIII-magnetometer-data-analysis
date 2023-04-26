#!/usr/bin/env python3
# define.py
# Hunter Barndt
# Purpose: Define global variables used throughout script tools

# ADD YOUR LOCAL DIR PATH TO THE DATA, THIS SCRIPT ASSUMES DATA ISN'T STORED IN THE LOCAL DIR 
current_machine = 'whbarndt-local'
directory_preambles = {
    'whbarndt-local' : 'D:/UAF/PHYS Capstone/',
}

### Date deines ###
num_months = 12
num_days = 31

gima_download_start_year = 2019
gima_download_end_year = 2022

reeves_start_year = 2010 # 2009 technically but unusable data
reeves_end_year = 2022
num_reeves_years = reeves_end_year - reeves_start_year
swugat_start_year = 2023
swugat_end_year = 2023

processing_start_year = 2010
processing_end_year = 2022
num_processing_years = processing_end_year - processing_start_year

### SWUG ATLAS DEFINES ###
swugat_website = "http://swugatlas.gi.alaska.edu"
swugat_sites_file_labels = [
    "pkr",
    "erc",
    "sol",
    "ili"
]
swugat_sites_dir_labels = [
    "poker",
    "eagle_river",
    "soldatna",
]
swugat_site = "eagle_river"

### GIMA DEFINES ###
gima_website = 'http://magnetometer.rcs.alaska.edu'
gima_sites = [
    "trapper"
]
selected_gima_site = 'trapper'

''' All gima sites
gima_sites = [
    "poker",
    "kaktovik",
    "arctic",
    "bettles",
    "toolik",
    "eagle",
    "trapper",
    "kenai",
    "cigo",
    "fortyukon",
    "gakona",
    "hlms",
    "homer",
]'''