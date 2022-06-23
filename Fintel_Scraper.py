

import time
import os
from pathlib import Path
import selenium
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from datetime import date
import yfinance as yf

ownership_data = {
    'File_Date':[], 
    'Source':[],
    'Investor':[],
    'Option_Type':[],
    'Avg_Share_Price':[],
    'Shares':[],
    'Shares_Changed(%)':[],
    'Value($1000)':[],
    'Value_Changed(%)':[]
    }

driver = webdriver.Chrome('C:/Users/robert.enright/chromedriver')  # Optional argument, if not specified will search path.

company_ticker = 'lcid'
tickerData = yf.Ticker(company_ticker)
SharePrice = tickerData.info['regularMarketPrice']
print(SharePrice)

driver.get('https://fintel.io/so/us/' + '{}'.format(company_ticker))

time.sleep(5)   # Give time for Sunset to generate the report

ownership_table = '//*[@id="transactions"]'

r = driver.find_elements_by_xpath (ownership_table + "/tbody/tr")
rc = len (r)

c = driver.find_elements_by_xpath (ownership_table + "/thead/tr/th")
cc = len (c)
print(cc)

for i in range (1, rc):
    ownership_data['File_Date'].append(driver.find_element_by_xpath (ownership_table + "/tbody/tr["+str(i)+"]/td["+str(1)+"]").text)
    ownership_data['Source'].append(driver.find_element_by_xpath (ownership_table + "/tbody/tr["+str(i)+"]/td["+str(2)+"]").text)
    ownership_data['Investor'].append(driver.find_element_by_xpath (ownership_table + "/tbody/tr["+str(i)+"]/td["+str(3)+"]").text)
    ownership_data['Option_Type'].append(driver.find_element_by_xpath (ownership_table + "/tbody/tr["+str(i)+"]/td["+str(5)+"]").text)
    ownership_data['Avg_Share_Price'].append(driver.find_element_by_xpath (ownership_table + "/tbody/tr["+str(i)+"]/td["+str(6)+"]").text)
    ownership_data['Shares'].append(driver.find_element_by_xpath (ownership_table + "/tbody/tr["+str(i)+"]/td["+str(7)+"]").text)
    ownership_data['Shares_Changed(%)'].append(driver.find_element_by_xpath (ownership_table + "/tbody/tr["+str(i)+"]/td["+str(8)+"]").text)
    ownership_data['Value($1000)'].append(driver.find_element_by_xpath (ownership_table + "/tbody/tr["+str(i)+"]/td["+str(9)+"]").text)
    ownership_data['Value_Changed(%)'].append(driver.find_element_by_xpath (ownership_table + "/tbody/tr["+str(i)+"]/td["+str(9)+"]").text)
   

ownership_df = pd.DataFrame.from_dict(ownership_data)
print(ownership_df.to_string())

driver.close()


