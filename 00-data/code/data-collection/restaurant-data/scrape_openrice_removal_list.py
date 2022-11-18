# Purpose: to scrape the restaurants to exclude from OpenRice
# Notes (08/04/2022):
## changed the time zone for my laptop to Hong Kong
## 2021 Legislative Council Election: 2021-12-19 (Remove those added after this date when analyzing this election)
## 2019 District Council Election: 2019-11-24 (Remove those added after this date when analyzing this election)

# To-Do:
## Fix those that didn't load in the dataset
## Fix those with "x days ago" based on the date 08/04/2022

# import libraries
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from time import sleep
import googlemaps
from datetime import datetime

# initialize chrome driver
s = Service('Enter the path to Chromedriver')
driver = webdriver.Chrome(service = s)
driver.get('https://www.openrice.com/zh/restaurant/userinfo.htm?userid=66275053&tc=MYOR');
#give time for all javascripts to be finished loading
sleep(60)
page = driver.page_source

soup = BS(page, "lxml")

# find rows
rows = soup.find_all('div', {'class': 'PL15'})
# initialize empty lists
date_added = []
restaurant_name = []
district = []

# loop in all rows to extract info
for i in range(len(rows)):
    temp_date_added = None
    temp_restaurant_name = None
    temp_district = None
    try: 
        temp_date_added = list(rows[i].find_all('div',{'class':'PB5 ng-binding'})[0])[0]
        temp_restaurant_name = list(rows[i].find_all('a',{'class':'txt_15 txt_bold ng-binding'})[0])[0]
        temp_district = list(rows[i].find_all('a',{'class':'hiddenlink ng-binding'})[0])[0]
    except:
        pass
    date_added.append(temp_date_added)
    restaurant_name.append(temp_restaurant_name)
    district.append(temp_district)

# save as a data frame
openrice_removal = list(zip(date_added, district, restaurant_name))
df_openrice_removal = pd.DataFrame(openrice_removal, columns = ['date_added', 'district', 'restaurant_name'])


# save as a csv file
df_openrice_removal.to_csv("openrice_removal.csv")
