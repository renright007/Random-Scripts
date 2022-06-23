

# This script usese BeautifulSoup to scrape the goals information of PL players for the tables that can be found on the offical Premier League Website. It demonstrates proficiencies in both Beautiful Soup and Pandas. 

# Import Libraries

from pathlib import Path
import selenium
import csv
import time
from datetime import date
import pandas as pd
import win32com
import win32com.client as win32
from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager

coin_data = {
    'Coin Symbol':[],
    'Price ($ USD)':[],
    'Hour % movement':[]
    #'9AM % Moved':[],
    #'12PM Price':[],
    #'12PM % Moved':[],
    #'5PM Price':[],
    #'5PM % Moved':[]
    }

# Open ChromeDrive

host = '192.168.12.12'  # Define the Host and Port
port = 12345

url = 'https://www.coingecko.com/en/coins/trending?time=h1'
driver = webdriver.Chrome(ChromeDriverManager().install())  # Define the Driver
driver.get(url) # Get the PL Websitre

driver.maximize_window()    # Maximize Window so the full screen information appears

table_name = '//*[@id="gecko-table-all"]'

r = driver.find_elements_by_xpath (table_name + "/tbody/tr")    # Get the row lenght
rc = len (r)
rc

time.sleep(2)   # Time to wait

# We must now loop through each player URL

for i in range (1, 30):

    coin_name = driver.find_element_by_xpath(table_name + "/tbody/tr[" +str(i) + "]/td[1]/div/div[2]/a").text
    price = driver.find_element_by_xpath(table_name + "/tbody/tr[" +str(i) + ']/td[3]/a/span').text
    hour_movement = driver.find_element_by_xpath(table_name + "/tbody/tr[" +str(i) + ']/td[4]/span').text


    coin_data['Coin Symbol'].append(coin_name)
    coin_data['Price ($ USD)'].append(price[1:])
    coin_data['Hour % movement'].append(hour_movement[:-1])

coins_df = pd.DataFrame.from_dict(coin_data)    # Convert to data frame
coins_df.index += 1
coins_df.index.name = 'Rank'
print(coins_df.to_string())

filepath = 'C:/Users/robert.enright/Downloads/CoinGeckoExtract/CG_extract_{today}.csv'.format(today = str(date.today()))

coins_df.to_csv(filepath)

outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'robert63.enright@gmail.com'
mail.Subject = 'CoinGecko Movers'
mail.Body = 'Hello Lads, \n Please find the list attached. \n Rob'
mail.HTMLBody = '<h2>HTML Message body</h2>' #this field is optional

# To attach a file to the email (optional):
attachment  = "filepath"
mail.Attachments.Add(attachment)

mail.Send()
