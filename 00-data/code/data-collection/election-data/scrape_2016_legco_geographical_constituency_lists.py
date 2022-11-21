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
from itertools import product


# functions to transform tables with rowspans and colspans
def table_to_2d(table_tag):
    rowspans = []  # track pending rowspans
    rows = table_tag.find_all('tr')

    colcount = 0
    for r, row in enumerate(rows):
        cells = row.find_all(['td', 'th'], recursive=False)

        colcount = max(
            colcount,
            sum(int(c.get('colspan', 1)) or 1 for c in cells[:-1]) + len(cells[-1:]) + len(rowspans))
        # update rowspan bookkeeping; 0 is a span to the bottom. 
        rowspans += [int(c.get('rowspan', 1)) or len(rows) - r for c in cells]
        rowspans = [s - 1 for s in rowspans if s > 1]

    # build an empty matrix for all possible cells
    table = [[None] * colcount for row in rows]

    # fill matrix from row data
    rowspans = {}  # track pending rowspans, column number mapping to count
    for row, row_elem in enumerate(rows):
        span_offset = 0  # how many columns are skipped due to rowspans and colspans 
        for col, cell in enumerate(row_elem.find_all(['td', 'th'], recursive = False)):
            # adjust for preceding row and colspans
            col += span_offset
            while rowspans.get(col, 0):
                span_offset += 1
                col += 1

            # fill table data
            rowspan = rowspans[col] = int(cell.get('rowspan', 1)) or len(rows) - row
            colspan = int(cell.get('colspan', 1)) or colcount - col
            # next column is offset by the colspan
            span_offset += colspan - 1
            value = cell.get_text()
            for drow, dcol in product(range(rowspan), range(colspan)):
                try:
                    table[row + drow][col + dcol] = value
                    rowspans[col + dcol] = rowspan
                except IndexError:
                    # rowspan or colspan outside the confines of the table
                    pass

        # update rowspan bookkeeping
        rowspans = {c: s - 1 for c, s in rowspans.items() if s > 1}

    return table

# ----------------------------------Scrape tables for each constituency
# provide the root url
root_url = 'https://www.elections.gov.hk/legco2016/eng/rs_gc_LC'
# initialize an empty data frame
df_hk_lce_2016 = pd.DataFrame()
# loop in each page for each constituency
# 5 geographical constituencies in total
for page in range(1, 6):
    # initialize chrome driver
    s = Service('Enter the path to Chromedriver')
    driver = webdriver.Chrome(service = s)
    # glue the url
    driver.get(root_url + str(page) + '.html');
    #give time for all javascripts to be finished loading
    sleep(10)
    page = driver.page_source
    # create a soup object
    soup = BS(page, "lxml")
    
    # find the table body
    table = soup.find('table', border = 1)

    # apply the pre-written function
    temp_table_transformed = table_to_2d(table)

    temp_df_table_transformed = pd.DataFrame(temp_table_transformed, columns = ['list_number', 'candidates',
                                                                                'votes_received', 'results'])
    temp_df_table_transformed = temp_df_table_transformed.iloc[2: , :]
    
    # concat the data frame
    df_hk_lce_2016 = df_hk_lce_2016.append(temp_df_table_transformed, ignore_index = True)

# save as a csv file
df_hk_lce_2016.to_csv('2016_legco_candidate_list.csv', index = False)



