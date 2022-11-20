# import libraries
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

# initialize chrome driver
driver = webdriver.Chrome(executable_path = 'enter path to your chromedriver')

# functions to transform tables to 2D
def table_to_2d(table_tag):
    rows = table_tag("tr")
    cols = rows[0](["td", "th"])
    table = [[None] * len(cols) for _ in range(len(rows))]
    for row_i, row in enumerate(rows):
        for col_i, col in enumerate(row(["td", "th"])):
            insert(table, row_i, col_i, col)
    return table

def insert(table, row, col, element):
    if row >= len(table) or col >= len(table[row]):
        return
    if table[row][col] is None:
        value = element.get_text()
        table[row][col] = value
        if element.has_attr("colspan"):
            span = int(element["colspan"])
            for i in range(1, span):
                table[row][col+i] = value
        if element.has_attr("rowspan"):
            span = int(element["rowspan"])
            for i in range(1, span):
                table[row+i][col] = value
    else:
        insert(table, row, col + 1, element)


####################################
## 2019 District Council Election ##
####################################

driver.get('https://www.elections.gov.hk/dc2019/eng/results_hk.html');
#give time for all javascripts to be finished loading
sleep(10)
page = driver.page_source

soup = BS(page, "lxml")

# find the table
table = soup.find('table', id = 'table-district-member')

# apply the function
table_2d = table_to_2d(table)

# save the table as a data frame
df_candidate = pd.DataFrame(table_2d, columns = ['Constituency Code','Constituency',
                                                  'Candidate Number','Name of Candidate',
                                                  'No. of Votes Received'])
# clean 
df_candidate = df_candidate.iloc[1: , :]
# save it to csv
df_candidate.to_csv('hk2019_district_election_candidate_shares.csv')


####################################
## 2015 District Council Election ##
####################################

driver.get('https://www.elections.gov.hk/dc2015/eng/results_hk.html?1659228802610');
#give time for all javascripts to be finished loading
sleep(10)
page = driver.page_source

soup = BS(page, "lxml")

# find the table
table = soup.find('table', {'class': 'contents2'})

# NOTE: There's a rowspan in Column 1 and 2 in this table. Transform it for scraping.
# apply the function
table_2d = table_to_2d(table)

# save the table as a data frame
df_candidate = pd.DataFrame(table_2d, columns = ['Constituency Code','Constituency',
                                                  'Candidate Number','Name of Candidate',
                                                  'No. of Votes Received'])
# clean 
df_candidate = df_candidate.iloc[1: , :]
# save it to csv
df_candidate.to_csv('hk2015_district_election_candidate_shares.csv')


####################################
## 2011 District Council Election ##
####################################

driver.get('https://www.elections.gov.hk/dc2011/eng/results_hk.html');
#give time for all javascripts to be finished loading
sleep(10)
page = driver.page_source

soup = BS(page, "lxml")

# find the table
table = soup.find('table', {'class': 'contents2'})

# save the table as a data frame
df_candidate = pd.DataFrame(table_2d, columns = ['Constituency Code','Constituency',
                                                  'Candidate Number','Name of Candidate',
                                                  'No. of Votes Received'])
# clean 
df_candidate = df_candidate.iloc[1: , :]

# save it to csv
df_candidate.to_csv('hk2011_district_election_candidate_shares.csv')