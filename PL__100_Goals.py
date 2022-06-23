# This script usese BeautifulSoup to scrape the goals information of PL players for the tables that can be found on the offical Premier League Website. It demonstrates proficiencies in both Beautiful Soup and Pandas.  


# Import Libraries

import pandas as pd
import requests
import urllib
import urllib.request
from bs4 import BeautifulSoup
import re


# Website URL defined below

pl_master_url = 'https://www.premierleague.com/stats/top/players/goals?co=1&se=-1&co=1&cl=-1&iso=-1&po=-1?se=-1'

# CONNECT TO PL URL

response = requests.get(pl_master_url)

# Step 2: Parse the html content

soup = BeautifulSoup(response.text, 'html.parser')

scorers_table = soup.find('div', class_='table statsTable') # Identify the name of the whole table area
table_data = scorers_table.find('table') # Find the actual table
table_body = table_data.find('tbody') # Find the body of the table - where the script begins

body_details = table_body.find_all('tr') # This contains all rows within the table

# Declare empty list to keep columns names

headings = ['Player', 'DOB', 'Season', 'Team', 'Apps', 'Goals']
goals_data = []

# Now we must collect locate each player's URL within the table

for pl_row in range(0, len(body_details)):

    url_row = body_details[pl_row].find('td', scopr='row') # Locate the row containing the name and player page URL

    player_name = str(url_row.text.strip()) # Get the name of player, strip the excess \n
    player_url = 'https://www.premierleague.com'+str(url_row.find('a', href=True).get('href')) # After locating 'a' which contains the href, we then extract it using the GET function from the urllib.request lib

    # Now we must collect the data from the player's page

    response_1 = requests.get(player_url)

    soup_1 = BeautifulSoup(response_1.text, 'html.parser')
    
    if soup_1.find('div', class_="table playerClubHistory true") == None:
        goals_table = soup_1.find('div', class_="table playerClubHistory playerClubHistory--hideRevealMore false")
    else:
        goals_table = soup_1.find('div', class_="table playerClubHistory true")
    goals_table_t = goals_table.find("table")
    goals_table_tbody =  goals_table_t.find("tbody")

    goals_body = goals_table_tbody.find_all("tr", class_="table")

    # Declare empty list to keep columns names

    headings = ['Player', 'DOB', 'Season', 'Team', 'Apps', 'Goals']

    dob_info = soup_1.find('ul', class_='pdcol2')         # pdcol2 contains the DoB information
    dob = dob_info.find('div', class_='info').text.strip()         # We just want to pull the info text

    for row_num in range(0,len(goals_body)): # Row at a time, in increments of two as every second row is blank

        row = [player_name,dob] # Blank list for row data
        row_data = (goals_body[row_num].find_all("td")) # Find all "td" data for each row within the body

        for row_item in range(0, len(row_data)-1): # Each piece of data at at a time (within the row), exlude "More" column

            if row_data[row_item] == row_data[1]: # Club name is duplicated, we must isolate one part of the text
                contents = row_data[row_item].find('span', class_="long").text
                row.append(contents) # Append to row
        
            elif row_data[row_item] == row_data[2]: # Get rid of subs apps data
                contents = row_data[row_item].text.strip()[:-4] # Remove of " (0)" at the end off all the appearance data
                row.append(contents) # Append to row

            else: # For all other data components
                contents = row_data[row_item].text.strip()
                row.append(contents) # Append to row
                
        goals_data.append(row) # Combine all the data

from pandas import DataFrame    # Import to DataFrame function from Pandas

df = DataFrame(goals_data, columns=headings)   # Convert our dictionary to a Dataframe as it is easier to manipulate

df['Goals'] = pd.to_numeric(df['Goals'])       # Convert Goals to a numeric form
df['Apps'] = pd.to_numeric(df['Apps'])         # Convert Apps to a numeric form

df = df[df['Apps'] != 0]                       # We do not want include any season where the player had 0 PL apps
df = df.drop_duplicates().reset_index(drop=True)                        # Remove duplicates

df['GPG Ratio'] = round(df['Goals'] / df['Apps'],2)           # The 'Goals per game ratio' is added to the DF which is goals divided by games

df['Age'] = ''       # The is an empty column which denotes the players age at the beginning of the season

from datetime import datetime     # To convert to age, we need to import the datatime library

for i in range(0, len(df)):

    dob = df['DOB'].iloc[i].strip()[:10].split('/')       # We need to strip the DOB to 10 characters as active players ages are at the end of the string. We must also split it into a list, with the '/' as the separator 
    final_dob = datetime(int(dob[2]),int(dob[1]),int(dob[0]))   # The final_dob is in datetime format to that it can be manipulated
    days_in_year = 365.2425   # The number of days in a year

    df['Age'].iloc[i] = round((datetime(int(df['Season'].iloc[i][:4]),8,15)-final_dob).days/days_in_year)    # We subtract the date at the start of the season with that the player's DOB, we then return the number of days and get the number in years.

print(df)
  

import csv

with pd.ExcelWriter('master_db.xlsx') as writer:
    df.to_excel(writer, sheet_name='master_db')