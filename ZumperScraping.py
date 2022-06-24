# Import Libraries

import datetime
from pathlib import Path
import selenium
import csv
import time
import signal 
import urllib
import pandas as pd
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

class GrabAptData:
    
    def __init__(self, url):
        self.url = url
        # self.append = append
        # self.listings_data = {'Listing Name':[], 'Listing URL':[], 'Managed By':[], 'Street Address':[], 'City':[], 'Postal Code':[], 'Units':[], 'Images':[], 'About':[]}
        self.unit_data = {'Unit Type':[], 'Specs':[], 'Bathrooms':[], 'Price':[], 'SQFT':[]}
        
    def OpenUrl(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)
        driver.get(self.url) # Get the PL Websitre
        driver.maximize_window()    # Maximize Window so the full screen information appears
        
        listing_xpath = '//*[@id="rail"]/div/div/div/div[2]/div[1]/div/div[1]/div/div/div[1]/img'
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, listing_xpath))).click()

        see_more_btn = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/div[4]/div/div[3]/div/button'
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, see_more_btn))).click()

        
        def grab_listing_data(self):
            # Grab the listing URL
            listing_url = driver.current_url

            # Listing Name details
            listing_name = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]/div/h1'))).text.split('\n')[0]

            # Get the management details
            managed_by_str = driver.find_element(by=By.XPATH, value='//div[@data-testid="details"]').text.split('\n')[0]

            if 'Managed by' in managed_by_str:
                managed_by = managed_by_str
            else:
                managed_by = 'Not listed'
                
            # Scrape full address and append details accordingly
            address = driver.find_element(by=By.XPATH, value='//div[@data-testid="details"]').text.split('\n')[1]
            address_list = address.split(' · ')[1].split(', ')
            # Define the address details
            street_address = address_list[0]
            city = address_list[1]  
            postal_code = address_list[2].split(" ")[1] + " " + address_list[2].split(" ")[2]  # Postal code requires additional split to identify PC prefix
                
            print(listing_url)
            print(listing_name)
            print(managed_by)
            print(street_address)
            print(city)
            print(postal_code)
        
        def grab_image_data(self):

            image_list = []    # Blank image list

            images = driver.find_elements(by=By.TAG_NAME, value='img')    # Find all image elements

            for image in images:    # Now we must locate the actual listing photos

                listing_prefix  = 'https://img.zumpercdn.com'   # We know that they have this prefix
                image_url = image.get_attribute('src')          # Get the image URL
                dim_suffix = '1280x960?fit=crop&h=900&w=1000'   # Define the format of the desired dimensions.

                if image_url is None:       # Ignore those that return None
                    pass

                elif listing_prefix in image_url:
                    # Split out the string and replace the existing suffice with our desired one
                    scaled_url = image_url.split('/')
                    scaled_url[-1] = dim_suffix

                    # Join the ammended list as a string and append to our list
                    scaled_url = '/'.join(scaled_url)
                    image_list.append(scaled_url)
                    
            print(image_list)
            
        def grab_fp_info(self):
            
            floorplans = driver.find_elements(by=By.CLASS_NAME, value='css-o6i9hf')
            fpc = len(floorplans)
            
            if fpc == 1:
                fp_table = "//*[@id='root']/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div[4]/div/div[1]/div/div/div["
            else:
                fp_table = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/div[4]/div/div[1]/div/div['                
            
            for j in range(1, fpc + 1):
                
                fp_click = driver.find_element(by=By.XPATH, value= fp_table + str(j) + ']/div[1]/div[2]/div[1]/div[1]')
                fp_click.click()    # Click floorplan to expand details
                
                fp_name = driver.find_element(by=By.XPATH, value= fp_table + str(j) + ']/div[2]/div/div/div[1]/div[2]/div[1]/div[1]').text
                fp_bath = driver.find_element(by=By.XPATH, value= fp_table + str(j) + ']/div[2]/div/div/div[1]/div[2]/div[2]').text
                fp_sqft = driver.find_element(by=By.XPATH, value= fp_table + str(j) + ']/div[2]/div/div/div[1]/div[2]/div[3]/span').text
                fp_price = driver.find_element(by=By.XPATH, value= fp_table + str(j) + ']/div[2]/div/div/div[1]/div[2]/div[1]/div[2]').text[1:]
            
            print(fp_name)
            print(fp_bath)
            print(fp_sqft)
            print(fp_price)
                                
        grab_listing_data(self)
        grab_image_data(self)
        grab_fp_info(self)
        driver.back()


        
        
    
        
        