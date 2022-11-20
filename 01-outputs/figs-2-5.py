# import libraries
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon

# load 2019 district council constituency shapefile for all figures in this script
# https://data.gov.hk/en-data/dataset/eac-eacpsi01-dcca-boundaries-2019
hk_shapefile = gpd.read_file('../hk_2019_dsc.shp')

##############
## Figure 2 ##
##############

# load data for protest sites
# HKU website: 
# https://datahub.hku.hk/articles/dataset/ANTIELAB_Research_Data_Archive_-_Mobilization_Map_Data/13711540

# set the geometry
crs = {'init':'epsg:4326'}
# read in the shape file for the protest/mobilization data
geodata = gpd.read_file('/Users/jiayili/Dropbox/Mac/Downloads/all/event.shp')
geodata = geodata['geometry']
# plot points
geodata.plot()

# create subplots
fig, ax = plt.subplots(figsize=(7,7))

# plot points onto the official district council constituency shapefile
hk_shapefile.plot(ax=ax, facecolor='Grey', edgecolor='k',alpha=0.2,linewidth=1,cmap="cividis")

geodata.plot(ax=ax, color='red', edgecolor = 'black', alpha = 0.2);

# set axis labels
ax.set_xlabel('Longitude', fontsize=10, fontname='Arial')
ax.set_ylabel('Latitude', fontsize=10, fontname='Arial')
# despine
sns.despine()
# save
fig.savefig('protest_sites.jpg', dpi=400)

##############
## Figure 5 ##
##############

# load raw restaurant data
restaurant_raw = pd.read_csv("../openrice_final_raw.csv")

# create two subsets based on political ideological labels
blue_restaurant_raw = restaurant_raw[restaurant_raw['ideo_text'] == 'Blue']

yellow_restaurant_raw = restaurant_raw[restaurant_raw['ideo_text'] == 'Yellow']

# Blue restaurants
# set the geometry
crs = {'init':'epsg:4326'}
geometry = [Point(xy) for xy in zip(blue_restaurant_raw["lon"], blue_restaurant_raw["lat"])]
geodata = gpd.GeoDataFrame(blue_restaurant_raw, crs = crs, geometry = geometry)
# plot the point
geodata.plot()

# create subplots
fig, ax = plt.subplots(figsize=(7,7))

# plot points onto the official district council constituency shapefile
hk_shapefile.plot(ax=ax, facecolor='Grey', edgecolor='k',alpha=0.2,linewidth=1,cmap="cividis")


geodata.plot(ax=ax, color='cornflowerblue', markersize=5);


# set axis labels
ax.set_xlabel('Longitude', fontsize=10, fontname='Arial')
ax.set_ylabel('Latitude', fontsize=10, fontname='Arial')
# despine
sns.despine()
# save
fig.savefig('blue_fig.jpg', dpi=400)

# Yellow restaurants
# set the geometry
crs = {'init':'epsg:4326'}
geometry = [Point(xy) for xy in zip(yellow_restaurant_raw["lon"], yellow_restaurant_raw["lat"])]
geodata = gpd.GeoDataFrame(yellow_restaurant_raw, crs = crs, geometry = geometry)
# plot the points
geodata.plot()

# create subplots
fig, ax = plt.subplots(figsize=(7,7))

# plot points onto the official district council constituency shapefile
hk_shapefile.plot(ax=ax, facecolor='Grey', edgecolor='k',alpha=0.2,linewidth=1,cmap="cividis")


geodata.plot(ax=ax, color='cornflowerblue', markersize=5);

# set axis labels
ax.set_xlabel('Longitude', fontsize=10, fontname='Arial')
ax.set_ylabel('Latitude', fontsize=10, fontname='Arial')
# despine
sns.despine()
# save
fig.savefig('yellow_fig.jpg', dpi=400)
