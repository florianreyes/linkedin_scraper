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


def query_formater(inp):
    final_query = 'site: linkedin.com/in /'
    inp = inp.split(' ')
    for word in inp:
        final_query += ' AND "{}"'.format(word)
    return final_query


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
        query_formater(query))
    search.send_keys(Keys.RETURN)
    time.sleep(3)
    # looping through each result and printing the URL.
    linkedin_resultados = driver.find_elements(
        By.CLASS_NAME, 'yuRUbf')
    linkedin_links = []
    for i in range(len(linkedin_resultados)):
        linkedin_links.append(linkedin_resultados[i].find_element(
            By.TAG_NAME, 'a').get_attribute('href'))
    return linkedin_links


def get_data(driver, urls):
    names = []
    descriptions = []
    companies = []
    for url in urls:
        driver.get(url)
        time.sleep(2)
        # Using the BeautifulSoup library to parse the HTML.
        soup = bs(driver.page_source, 'html.parser')
        # Using the BeautifulSoup library to find the name of the person.
        try:
            names.append(
                soup.find("h1", class_='text-heading-xlarge').text.strip())
        except:
            pass
        try:
            descriptions.append(soup.find(
                "div", class_='text-body-medium').text.strip())
        except:
            descriptions.append("-")
        try:
            companies.append(driver.find_element(
                By.XPATH, "/html/body/div[6]/div[3]/div/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/ul/li[1]/button/span/div").text.strip())
        except:
            companies.append("-")

    final_index = [[companies[i], names[i], descriptions[i], urls[i]]
                   for i in range(len(urls))]
    return final_index


def list_to_csv(l):
    df = pd.DataFrame(l, columns=[
        'Company', 'Name', 'Description', 'URL'])
    df.to_csv('linkedin_profiles.csv', index=False)


def main():
    query = input("What job are you looking for? ")
    # Using the Selenium webdriver to open a Chrome browser.
    driver = webdriver.Chrome(config.PATH)
    # Calling login function to log in to LinkedIn.
    linkedin_login(driver)
    time.sleep(2)
    # Calling google_search function to look for linkedin profiles.
    urls = google_search(driver, query)
    data = get_data(driver, urls)
    list_to_csv(data)


if __name__ == "__main__":
    main()
