# Purpose: to clean Maxim's restaurant data scraped by Python
# To-Do (07/29/2022):
#  - Cleaning:
#   -- Merge all the datasets for each individual cuisine
#   -- Drop the index column
#   -- Drop restaurants in Shenzhen
#   -- Add a column to indicate the corporate

# Notes: 
# - Didn't scrape the 2 catering businesses owned by Maxim's

# load packages
  source("../data-cleaning/helper-packages.R")

# load data: enter the path to the folder with all Maxim's data
  path <- "../working-data/maxims-raw/"
# get file names
# 33 files in total
  data_files <- list.files(path)

# loop in all file names to load data
  for(i in 1:length(data_files)) {                              
    assign(paste0("maxims_", i),                                   
           read.csv(paste0(path,
                            data_files[i])))
  }

  # bind rows and remove the index column
  maxims_raw <-
    # merge all loaded data sets by cuisine
    do.call("rbind", mget(ls(pattern = "^maxims_*"))) %>%
    # drop the index columns
    select(-1)

# reset index
  row.names(maxims_raw) <- NULL
  
# check duplicates
  sum(duplicated(maxims_raw$restaurant_name))
  
# clean duplicates and correct mistakes in locations from scraping
  clean_maxims <-
    maxims_raw %>%
    # drop mistakes on locations from scraping
    filter(location != "Total 12 results found") %>%
    # drop restaurants in Shenzhen
    filter(location != "Shenzhen") %>%
    # drop duplicates
    distinct(.keep_all = TRUE) %>%
    mutate(
      # add a column for the corporate
      corporate = "Maxim's"
    ) %>%
    # rearrange the column order
    relocate(corporate)