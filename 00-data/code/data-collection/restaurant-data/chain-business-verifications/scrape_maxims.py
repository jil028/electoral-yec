# Purpose: to scrape data for Maxim's restaurants in Hong Kong
# To-Do (07/26/2022):

# Extracting variables of interest:
# Restaurant Name
# Location
# Cuisine

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
# urls to scrape by cuisine type:
## cantonese:
#  - https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=1&d=All&k=&p=1&m=1
#  - https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=1&d=All&k=&p=2&m=1

## chiu chow:
# https://www.maxims.com.hk/en/search/restaurantsearch.asp?c=2&d=All&k=

## provincial:
# https://www.maxims.com.hk/en/search/restaurantsearch.asp?c=3&d=All&k=

## wetsern:
# https://www.maxims.com.hk/en/search/restaurantsearch.asp?c=4&d=All&k=

## Japanaese:
# https://www.maxims.com.hk/en/search/restaurantsearch.asp?c=5&d=All&k=
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=5&d=All&k=&p=2&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=5&d=All&k=&p=3&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=5&d=All&k=&p=4&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=5&d=All&k=&p=5&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=5&d=All&k=&p=6&m=1

## vietnamese and thai
# https://www.maxims.com.hk/en/search/restaurantsearch.asp?c=6&d=All&k=

## fast food
# https://www.maxims.com.hk/en/search/restaurantsearch.asp?c=7&d=All&k=
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=7&d=All&k=&p=2&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=7&d=All&k=&p=3&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=7&d=All&k=&p=4&m=1


# choose url from the above 
# definitely can do regular expression on the link above and then a for loop
# but i was too tired to write the loop
driver.get('enter the link');
#give time for all javascripts to be finished loading
sleep(10)
page = driver.page_source

soup = BS(page, "lxml")

# find the div
div = soup.find('div', id = 'content_l')
table = div.find('table')
rows = table.find_all('tr')


# initialize empty lists for each variable of interest
restaurant_name = []
location = []
cuisine_type = []
# write the loop to extract info
for i in range(len(rows)):
    temp_restaurant_name = None
    temp_location = None
    temp_cuisine_type = None
    try:
        temp_restaurant_name = list(rows[i].find_all('td',{'class':'shoplink'})[0])[0]
        temp_location = list(rows[i].find_all('td',{'class':'general_txt'})[0])[1]
        temp_cuisine_type = list(rows[i].find_all('td',{'class':'general_txt'})[1])[1]
    except:
        pass
    restaurant_name.append(temp_restaurant_name)
    location.append(temp_location)
    cuisine_type.append(temp_cuisine_type)

# merge lists
maxims = list(zip(restaurant_name, location, cuisine_type))
df_maxims = pd.DataFrame(maxims, columns = ['restaurant_name', 'location', 'cuisine_type'])

# clean
df_maxims = df_maxims.dropna(subset=['restaurant_name'], how='all')
# remember to change this total number for every cuisine type
df_maxims = df_maxims[df_maxims.location != "Total 61 results found"].reset_index(drop = True)



# FOR CAKES AND BAKERY ONLY
# next time i will definitely do regular expressions + loop if there's next time
# https://www.maxims.com.hk/en/search/restaurantsearch.asp?c=8&d=All&k=
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=8&d=All&k=&p=2&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=8&d=All&k=&p=3&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=8&d=All&k=&p=4&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=8&d=All&k=&p=5&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=8&d=All&k=&p=6&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=8&d=All&k=&p=7&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=8&d=All&k=&p=8&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=8&d=All&k=&p=9&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=8&d=All&k=&p=10&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=8&d=All&k=&p=11&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=8&d=All&k=&p=12&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=8&d=All&k=&p=13&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=8&d=All&k=&p=14&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=8&d=All&k=&p=15&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=8&d=All&k=&p=16&m=1
# https://www.maxims.com.hk/en/search/restaurantSearch.asp?c=8&d=All&k=&p=17&m=1

# initialize chrome driver
driver = webdriver.Chrome(executable_path = 'enter the path to your Chrome driver')

# provide url from the above
driver.get('enter the link');
#give time for all javascripts to be finished loading
sleep(10)
page = driver.page_source

soup = BS(page, "lxml")

# find the div
div = soup.find('div', id = 'content_l')
table = div.find('table')
rows = table.find_all('tr')

# for cakes and bakery only
# initialize empty lists for each variable of interest
restaurant_name = []
location = []
cuisine_type = []
# write the loop to extract info
for i in range(len(rows)):
    temp_restaurant_name = None
    temp_location = None
    temp_cuisine_type = None
    try:
        temp_restaurant_name = list(rows[i].find_all('td',{'class':'shoplink'})[0].get_text(strip=True).split(','))[0]
        temp_location = list(rows[i].find_all('td',{'class':'general_txt'})[0])[1]
        temp_cuisine_type = list(rows[i].find_all('td',{'class':'general_txt'})[1])[1]
    except:
        pass
    restaurant_name.append(temp_restaurant_name)
    location.append(temp_location)
    cuisine_type.append(temp_cuisine_type)

# merge lists
maxims = list(zip(restaurant_name, location, cuisine_type))
df_maxims = pd.DataFrame(maxims, columns = ['restaurant_name', 'location', 'cuisine_type'])

# clean
df_maxims = df_maxims.dropna(subset=['restaurant_name'], how='all')
# remember to change this for every cuisine type
df_maxims = df_maxims[df_maxims.location != "Total 259 results found"].reset_index(drop = True)
display(df_maxims)

# save to csv
df_maxims.to_csv('maxims_cakes_bakery_n.csv')