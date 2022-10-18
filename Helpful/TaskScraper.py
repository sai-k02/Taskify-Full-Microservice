"""
Author: Srilokh Karuturi
Date: Tue Mar 15 2022
File: TaskScraper.py
Purpose: FETCH DATA FROM WEB 
License: MIT
"""

# imports
from aiohttp import request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from bs4 import BeautifulSoup
import time
import robot
import soupsieve
import requests
import dateutil
import datetime
import secrets
from dateutil.relativedelta import relativedelta


# TaskScraper Class
class TaskScraper():
    # MAIN
    @staticmethod
    def main(USERPREF):
        # DEFINE PATH
        PATH = "/Users/srilokh/Desktop/WebscrapingInstagram/chromedriver"
        
        # SET UP DRIVER
        driver = webdriver.Chrome(PATH)

        # SEND DRIVER TO HOME 
        driver.get("http://elearning.utdallas.edu/")
        
        # SLEEP
        time.sleep(5)

        # MAKE SURE WE CAN ENTER THE USERNAME AND PASSWORD
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="netid"]')))

        # INPUT USERNAME
        username = driver.find_element(By.XPATH, '//*[@id="netid"]')
        username.send_keys(secrets.USERNAME)

        # INPUT PASSWORD
        password = driver.find_element(By.XPATH,'//*[@id="password"]')
        password.send_keys(secrets.PASSWORD)

        # PRESS ENTER
        password.send_keys(Keys.RETURN)


        # SLEEP 
        time.sleep(3)

        # SET CURRENT DATE
        currentDate = datetime.date.today()

        # SET THE DATE ONE MONTH OUT FROM NOW 
        sinceDate = currentDate + relativedelta(months=1)

        # GO TO API CALL FOR BLACKBOARD BASED ON USER PREF
        if(USERPREF == 1):
            driver.get("https://elearning.utdallas.edu/learn/api/public/v1/calendars/items?since="+str(currentDate)+"&until="+str(sinceDate))
        elif(USERPREF == 0):
            driver.get("https://elearning.utdallas.edu/learn/api/public/v1/calendars/items?since=2022-01-01&until="+str(sinceDate))
        
        # GO AHEAD AND JUST TAKE THE HTML 
        html_doc = driver.page_source

        # USE SOUP TO PARSE HTML 
        soup = BeautifulSoup(html_doc, 'html.parser')

        # OPEN
        f = open("tasks.txt", "w")

        # WRITE
        f.write(soup.prettify())

        # CLOSE
        f.close()
    



