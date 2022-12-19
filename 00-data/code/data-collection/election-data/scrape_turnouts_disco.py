# import libraries
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from time import sleep
from itertools import product

# initialize chrome driver
s = Service('enter the path to chrome driver')
driver = webdriver.Chrome(service = s)

# functions to read and transform tables
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

 # 2019 District Council Election-------------------------------------------
driver.get('https://www.elections.gov.hk/dc2019/eng/turnout_numsum.html');
#give time for all javascripts to be finished loading
sleep(10)
page = driver.page_source

soup = BS(page, "lxml")
# find the table
table = soup.find('table', id = 'table-district-member')
# apply the function
table_2d = table_to_2d(table)
# save as data frame
df = pd.DataFrame(table_2d, columns = ['district', 'electoral_size',
                                       'aggregate_voter_turnout',
                                       'aggregate_voter_turnout_rate'])
# ad hoc cleaning
df_clean = df.iloc[1: , :]
#df_clean

# save to csv
df_clean.to_csv('turnouts_2019_disco.csv')




# 2015 District Council Election-------------------------------------------
driver.get('https://www.elections.gov.hk/dc2015/eng/turnout_numsum.html?1671414652601');
#give time for all javascripts to be finished loading
sleep(10)
page = driver.page_source

soup = BS(page, "lxml")
# find the table
table = soup.find('table', {'class': 'contents2'})
# apply the function
table_2d = table_to_2d(table)
# save as data frame
df = pd.DataFrame(table_2d, columns = ['district', 'electoral_size',
                                       'aggregate_voter_turnout',
                                       'aggregate_voter_turnout_rate'])
# ad hoc cleaning
df_clean = df.iloc[1: , :]
#df_clean

# save to csv
df_clean.to_csv('turnouts_2015_disco.csv')



# 2011 District Council Election-------------------------------------------
driver.get('https://www.elections.gov.hk/dc2011/eng/turnout_numsum.html');
#give time for all javascripts to be finished loading
sleep(10)
page = driver.page_source

soup = BS(page, "lxml")
# find the table
table = soup.find('table', {'class': 'contents2'})
# apply the function
table_2d = table_to_2d(table)
# save as data frame
df = pd.DataFrame(table_2d, columns = ['district', 'electoral_size',
                                       'aggregate_voter_turnout',
                                       'aggregate_voter_turnout_rate'])
# ad hoc cleaning
df_clean = df.iloc[1: , :]
#df_clean

# save to csv
df_clean.to_csv('turnouts_2011_disco.csv')