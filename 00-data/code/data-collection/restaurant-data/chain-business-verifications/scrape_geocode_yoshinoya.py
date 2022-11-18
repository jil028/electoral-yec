# Purpose: to scrape and geocode data for Yoshinoya restaurants in Hong Kong
# To-Do (08/01/2022):

# Extracting variables of interest:

# Restaurant Name
# Address
# Geocoding locations of those restaurants using Google API:

# Latitude
# Longitude

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

# initialize chrome driver
driver = webdriver.Chrome(executable_path = 'Enter the path to your Chrome Driver')
driver.get('https://www.yoshinoya.com.hk/store-location/');
#give time for all javascripts to be finished loading
sleep(10)
page = driver.page_source

soup = BS(page, "lxml")

# find each div for the restaurant
div = soup.find('div', id = 'wpsl-stores')

# extract the restaurant's name    
restaurant_name_rows = div.find_all('strong')
# initialize an empty list
restaurant_name = []
# loop in 
for r in restaurant_name_rows:
        restaurant_name.append(r.text)
# clean the list
restaurant_name = pd.DataFrame(restaurant_name, columns = ["name"])
restaurant_name = restaurant_name[restaurant_name != "T"].reset_index(drop = True)
restaurant_name = restaurant_name.dropna()
restaurant_name = restaurant_name['name'].tolist()



# extract the address
address_rows = soup.find_all('span', {'class': 'wpsl-street'})
# initialize an empty list
address = []
# loop in 
for a in address_rows:
    address.append(a.text)

# save as a data frame
yoshinoya = list(zip(restaurant_name, address))
df_yoshinoya = pd.DataFrame(yoshinoya, columns = ['restaurant_name', 'address'])

# api
gmaps = googlemaps.Client(key = 'Enter your Google Maps API key')

# function to get coordinates
def glookup(names):
    # initialize lists
    geocode_result = []
    coordinates = []
    # loop in names of polling stations
    for i in range(len(names)):
        geocode_result.append(gmaps.geocode(names[i]))
        location = geocode_result[i][0]['geometry']['location'] if bool(geocode_result[i]) else None
        #print(i)
        coordinates.append([location['lat'], location['lng']]) if location is not None else coordinates.append([0,0])
    return coordinates


# get coordinates
gmaps_coords = glookup(address)

# assign back to the master data frame
df_yoshinoya['gmaps_coords'] = gmaps_coords

# save to csv
df_yoshinoya.to_csv('yoshinoya_hk.csv')