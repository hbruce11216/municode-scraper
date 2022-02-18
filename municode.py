import pandas as pd 
import os 
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import requests

def list_of_towns():
    driver = webdriver.Chrome('/Users/holdenbruce/Downloads/chromedriver3')

    # set implicit wait time so that apis/javascript load before we scrape 
    driver.implicitly_wait(5) # seconds

    # url of the county
    url = f"https://library.municode.com/VA"
    # headers to let them know who i am
    headers = {'user-agent': 'class project (hab6xf@virginia.edu)'}
    # xpath of the table in the webpage created by javascript 
    xpathHOME = "/html/body/div[1]/div[2]/ui-view/div[2]/section/div/div"

    driver.get(url)

    # use xpath to get to the table
    data = driver.find_elements_by_xpath(xpathHOME)
    # links = driver.find_elements_by_tag_name("a")
    
    # add a delay of 3 seconds in the function
    time.sleep(2)
    
    # use outerHTML to maintain the html/css/javasript code pulled from the webpage 
    html = data[0].get_attribute("outerHTML")

    r1 = re.findall(r"https://library.municode.com/VA/[\w\.-]+",html)

    # convert to dataframe and drop duplicates
    towns_list = pd.DataFrame(r1)
    towns_list = towns_list.drop_duplicates().reset_index(drop=True)

    return towns_list



def identify_comparison_table_URL_part1(url):
    driver = webdriver.Chrome('/Users/holdenbruce/Downloads/chromedriver')

    # set implicit wait time so that apis/javascript load before we scrape 
    driver.implicitly_wait(5) # seconds

    # url of the county
    # url = f"https://library.municode.com/va/{town}/codes/code_of_ordinances"
    # headers to let them know who i am
    # headers = {'user-agent': 'class project (hab6xf@virginia.edu)'}
    # xpath of the table in the webpage created by javascript 
    xpath = "/html/body/div[1]/div[2]/ui-view/mcc-codes/div[2]/section[1]/div[2]"

    driver.get(url)

    # use xpath to get to the table
    data = driver.find_elements_by_xpath(xpath)
    # links = driver.find_elements_by_tag_name("a")
    
    
    # add a delay of 3 seconds in the function
    time.sleep(2)
    
    
    # use outerHTML to maintain the html/css/javasript code pulled from the webpage 
    html = data[0].get_attribute("outerHTML")

    r2 = re.findall(r'(https?://[^\s]+)', html)
    
    url = r2[-1]
    url = url[:-1]
    
    return url




def scraper(url,town):
    driver = webdriver.Chrome('/Users/holdenbruce/Downloads/chromedriver')

    # set implicit wait time so that apis/javascript load before we scrape 
    driver.implicitly_wait(5) # seconds

    # url of the county
    url = identify_comparison_table_URL_part1(url)

    # xpath of the table in the webpage created by javascript 
    xpath = "/html/body/div[1]/div[2]/ui-view/mcc-codes/div[2]/section/div[1]/mcc-codes-content/div/div[2]/ul/li/mcc-codes-content-chunk/div/div/div[2]/div/div/div/div[2]/table"
    driver.get(url)

    # use xpath to get to the table
    data = driver.find_elements_by_xpath(xpath)
    
    # use outerHTML to maintain the html/css/javasript code pulled from the webpage 
    table = data[0].get_attribute("outerHTML")

    # https://stackoverflow.com/questions/41214702/parse-html-and-read-html-table-with-selenium-python

    # convert that table into a pandas dataframe
    df = pd.read_html(table)
    df = df[0]


    # rename the columns
    df = df.rename(columns={'Code of Virginia  Section': "Virginia", "Section this Code":town})


    # now write to CSV
    df.to_csv(f'countyCSV/{town}.csv', index=False)  
    
    return df