from pathlib import Path
import selenium
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome

movie_data = {
    'Rank':[], 
    'Title':[],
    'Year':[],
    'Score':[]
    }

driver = webdriver.Chrome('C:/Users/robert.enright/chromedriver')  # Optional argument, if not specified will search path.
driver.get('https://www.imdb.com/chart/top/')

top_table = "//*[@id='main']/div/span/div/div/div[3]/table"

r = driver.find_elements_by_xpath (top_table + "/tbody/tr")
rc = len (r)
print(rc)


c = driver.find_elements_by_xpath (top_table + "/thead/tr/th")
cc = len (c)
print(cc)


for i in range (1, rc+1):
    movie_data['Rank'].append(driver.find_element_by_xpath (top_table + "/tbody/tr["+str(i)+"]/td["+str(2)+"]").text.split(".")[0])

    title_list = driver.find_element_by_xpath (top_table + "/tbody/tr["+str(i)+"]/td["+str(2)+"]").text.split(".")

    if len(title_list) > 2:
        movie_data['Title'].append('.'.join(title_list[1:])[1:-8].strip())
    else:
        movie_data['Title'].append(driver.find_element_by_xpath (top_table + "/tbody/tr["+str(i)+"]/td["+str(2)+"]").text.split(".")[1][1:-8].strip())

    movie_data['Year'].append(driver.find_element_by_xpath (top_table + "/tbody/tr["+str(i)+"]/td["+str(2)+"]").text[-5:-1])
    movie_data['Score'].append(driver.find_element_by_xpath (top_table + "/tbody/tr["+str(i)+"]/td["+str(3)+"]").text)

movies_df = pd.DataFrame.from_dict(movie_data)
print(movies_df.to_string())

driver.close()

movies_df.to_csv('C:/Users/robert.enright/IMDB250.csv', index=False)