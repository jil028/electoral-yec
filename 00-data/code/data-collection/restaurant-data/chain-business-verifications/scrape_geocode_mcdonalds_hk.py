# Purpose: to scrape and geocode data for McDonald's restaurants in Hong Kong
# To-Do (07/26/2022):
# - Extracting variables of interest:
#     - Restaurant Name
#     - Address

# - Geocoding locations of those restaurants using Google API:
#     - Latitude
#     - Longitude



# import libraries
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import googlemaps
from datetime import datetime


# Get the data using selenium
# because HTML code containing restaurant info is rendered with JavaScript in the browser at runtime
# BeautifulSoup won't work

# initialize chrome driver
driver = webdriver.Chrome(executable_path = 'Enter the path to your Chrome Driver')
# provide url
driver.get('https://www.mcdonalds.com.hk/en/find-a-restaurant/');
#give time for all javascripts to be finished loading
sleep(10)
page = driver.page_source

# create soupe object
soup = BS(page, "lxml")


# Use BeatifulSoup to find restaurant names
restaurant_name_rows = soup.find_all('div', {'class': 'restaurant_name font_bold ng-binding'})
# initialize an empty list
restaurant_name = []
# loop in 
for r in restaurant_name_rows:
    restaurant_name.append(r.text)

# Use BeatifulSoup to find restaurant addresses
address_rows = soup.find_all('div', {'class': 'restaurant_address ng-binding'})
# initialize an empty list
address = []
# loop in 
for a in address_rows:
    address.append(a.text)
    
# Use BeatifulSoup to find restaurant tels
tel_rows = soup.find_all('div', {'class': 'restaurant_tel ng-binding'})
# initialize an empty list
tel = []
# loop in 
for t in tel_rows:
    tel.append(t.text)




# save as a data frame
mcdonalds = list(zip(restaurant_name, address, tel))
df_mcdonalds = pd.DataFrame(mcdonalds, columns = ['restaurant_name', 'address', 'tel'])
df_mcdonalds




# Geocode locations of the restaurants

# api
gmaps = googlemaps.Client(key = 'Enter your API key')

# function to get coordinates
def glookup(names):
    # initialize lists
    geocode_result = []
    coordinates = []
    # loop in names of polling stations
    for i in range(len(names)):
        geocode_result.append(gmaps.geocode(names[i]))
        location = geocode_result[i][0]['geometry']['location'] if bool(geocode_result[i]) else None
        print(i)
        coordinates.append([location['lat'], location['lng']]) if location is not None else coordinates.append([0,0])
    return coordinates


# get coordinates
gmaps_coords = glookup(address)

# assign back to the master data frame
df_mcdonalds['gmaps_coords'] = gmaps_coords


# look at the data frame
df_mcdonalds


# function to check bad addresses
def bad_names(row):
    if row['gmaps_coords'] == [0, 0]:
        return 1
    else:
        return 0
    
# check bad coordinates --> manually correct it later
df_mcdonalds['bad_names'] = df_mcdonalds.apply(bad_names, axis = 1)
display(df_mcdonalds['bad_names'].value_counts())

# save to csv
df_mcdonalds.to_csv('mcdonalds_hk.csv')

