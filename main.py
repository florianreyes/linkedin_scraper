from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import re as re
import time
import pandas as pd
import config as config

URL = "https://www.linkedin.com"


def linkedin_login(driver):
    driver.get(URL)
    # locate email form by id
    email = driver.find_element(By.ID, "session_key")
    # send_keys() to simulate key strokes
    email.send_keys(config.USERNAME)

    # locate password form by id
    password = driver.find_element(By.ID, "session_password")
    # send_keys() to simulate key strokes
    password.send_keys(config.PASSWORD)

    # locate submit button by class name
    submit_button = driver.find_element(
        By.CLASS_NAME, "sign-in-form__submit-button")
    # .click() to mimic button click
    submit_button.click()
    time.sleep(2)


def google_search(driver, query):
    # Using the webdriver to open Google.
    driver.get('https://www.google.com')
    time.sleep(3)
    # Using the webdriver to find the search bar and enter our search query.
    search = driver.find_element(By.NAME, 'q')
    search.send_keys(
        'site:linkedin.com/in/ AND "{}" AND "Argentina"'.format(query))
    search.send_keys(Keys.RETURN)
    time.sleep(3)
    # looping through each result and printing the URL.
    linkedin_resultados = driver.find_elements(
        By.CLASS_NAME, 'yuRUbf')
    for i in range(len(linkedin_resultados)):
        print(linkedin_resultados[i].find_element(
            By.TAG_NAME, 'a').get_attribute('href'))


if __name__ == "__main__":
    query = input("What job are you looking for? ")
    # Using the Selenium webdriver to open a Chrome browser.
    driver = webdriver.Chrome(config.PATH)
    # Calling login function to log in to LinkedIn.
    linkedin_login(driver)
    time.sleep(2)
    # Calling google_search function to look for linkedin profiles.
    google_search(driver, query)
    # doc = bs(driver.page_source, 'html.parser')
