# This script usese BeautifulSoup to scrape the goals information of PL players for the tables that can be found on the offical Premier League Website. It demonstrates proficiencies in both Beautiful Soup and Pandas. 

# Import Libraries

from pathlib import Path
import selenium
import csv
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager

# Define the goals dictionary

goals_data = {
    'Player':[],
    'Season':[],
    'Club':[],
    'Games':[],
    'Goals':[]
    }

def PL_goals_grab(url, page):

    # Open ChromeDrive

    host = '192.168.12.12'  # Define the Host and Port
    port = 12345

    driver = webdriver.Chrome(ChromeDriverManager().install())  # Define the Driver, while using ChromeDriverManager to ensure correct version is installed
    driver.get(url) # Get the PL Websitre

    time.sleep(2)  # Time to rest prior to removing cookie pop up

    # Click to dismiss the cookies button
    cookies_btn = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[5]/button[1]')
    cookies_btn.click() 

    driver.maximize_window()    # Maximize Window so the full screen information appears

    # Select the appropriate filter to display all time goals scoring data
    season_filter = driver.find_element_by_xpath("//*[@id='mainContent']/div[2]/div/div[2]/div[1]/section/div[1]/div[2]")
    season_filter.click()

    season_slct = driver.find_element_by_xpath("//*[@id='mainContent']/div[2]/div/div[2]/div[1]/section/div[1]/ul/li[1]")
    season_slct.click() 

    time.sleep(2)  # Time to rest prior to removing cookie pop up

    # Navigate to page outlined in the function. We need to use a for loop.
    for _ in range(page-1):
        page_btn = driver.find_element_by_xpath("//*[@id='mainContent']/div[2]/div/div[2]/div[1]/div[3]/div[2]")
        page_btn.click()

    # Now we must locate the goals list table

    pl_goals_table = "//*[@id='mainContent']/div[2]/div/div[2]/div[1]/div[2]/table" # Here is the xref path

    r = driver.find_elements_by_xpath (pl_goals_table + "/tbody/tr")    # Get the row lenght
    rc = len (r)

    time.sleep(2)   # Time to wait

    # We must now loop through each player URL

    for i in range (1, rc+1):
        
        driver.switch_to.window(driver.window_handles[0])   # Switch back to goals list page

        player_name = driver.find_element_by_xpath(pl_goals_table + "/tbody/tr[" +str(i) + "]/td[2]/a/strong").text             # Get players name
        player_url = driver.find_element_by_xpath(pl_goals_table + "/tbody/tr[" +str(i) + "]/td[2]/a").get_attribute('href')    # Get the player's underlying URL
    
        driver.execute_script("window.open('{url}','_blank')".format(url = player_url))     # Open the player's goals page in a new tab
        driver.switch_to.window(driver.window_handles[i])   # Switch to newly opened window

        try:
            table = driver.find_element_by_xpath("//*[@id='mainContent']/div[3]/div/div/div[3]/table")  # Some player's have a different table count, this caters to those with only 2
        except:
            table = driver.find_element_by_xpath("//*[@id='mainContent']/div[3]/div/div/div[2]/table")    # Define the path to the goals table

        for row in table.find_elements_by_xpath('.//tr[@class="table"]'):   # Isolate all the table rows where class is table to avoid cup goals
    
            row_data = row.text.split('\n')                 # Split into more malleable list
            row_data.append(row_data[2].split(' ')[-1])     # Append goals data
            row_data[2] = row_data[2].split(' ')[0]         # Format games data

            # Append information to goals dictionary
            goals_data['Player'].append(player_name)
            goals_data['Season'].append(row_data[0])
            goals_data['Club'].append(row_data[1])
            goals_data['Games'].append(row_data[2])
            goals_data['Goals'].append(row_data[3])


PL_goals_grab('https://www.premierleague.com/stats/top/players/goals?se=418', 1)
PL_goals_grab('https://www.premierleague.com/stats/top/players/goals?se=418', 2)

goal_df = pd.DataFrame.from_dict(goals_data)    # Convert to data frame
print(goal_df.to_string())