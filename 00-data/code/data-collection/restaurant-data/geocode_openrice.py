# import libraries
import numpy as np
import pandas as pd
import googlemaps
from datetime import datetime
import requests

# load the data
openrice_raw = pd.read_csv('../clean_openrice_not_geocoded.csv', index_col = [0])
openrice_raw.head()

# Enter API key
gmaps = googlemaps.Client(key = 'Enter your Google Maps API key here')

# function to geocode locations
def glookup(names):
	# initialize empty lists
	geocode_result = []
	coordinates = []
	# loop in each restaurant's name to geocode
	for i in range(len(names)):
		geocode_result.append(gmaps.geocode(names[i]))
		location = geocode_result[i][0]['geometry']['location'] if bool(geocode_result[i]) else None
		# showing the progress
		print(i) 
		coordinates.append([location['lat'], location['lng']]) if location is not None else coordinates.append([0,0])
	return coordinates

# convert to list
address = list(openrice_raw['address'])

# apply the function
gmaps_coords = glookup(address)

# assign coordinates back to the data frame
openrice_raw['gmaps_coords'] = gmaps_coords

# function to check bad addresses
def bad_names(row):
    if row['gmaps_coords'] == [0,0]:
        return 1
    else:
        return 0
    
# check bad coordinates --> manually correct them later
openrice_raw['bad_names'] = openrice_raw.apply(bad_names, axis = 1)
openrice_raw['bad_names'].value_counts()

# save as csv
openrice_raw.to_csv('geocoded_openrice.csv')



