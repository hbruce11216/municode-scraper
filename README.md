# municode-scraper

This scraper has 3 functions

- list_of_towns() scrapes the State-wide webpage and returns a single-column dataframe containing the links to each town/county's webpage on Municode
- identify_comparison_table_URL_part1() scrapes the town/county webpage and identifies the part of the webpage that contains information about state vs local law codes
  - This needs to be improved for accuracy. I currently wrote it to just take the last url on the page but that should be amended to actually search for the page that holds the table comparing state and local law codes. The subpages that hold this table have different names depending on the county.
- scraper() takes in the subpage url that was identified in identify_comparison_table_URL_part1() and scrapes the webpage, returning a two-column dataframe with the State law codes in the first column and the corresponding town/county law codes in the second column. The scraper() function then saves down this dataframe into a CSV, which can be found in the countyCSV folder.
  - This needs to be improved for specificity around what is being scraped. Some subpages contain multiple tables, some contain tables of different dimensions (4 columns instead of 2 columns) -- these differences need to be accounted for so that the right information is being returned in the dataframe.
