import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

#Loads all the variables
load_dotenv()


@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def login(browser):
    
    # Gets the URL and opens the website in browser
    browser.get(os.getenv('URL'))

    #This will locate the web element of username, password and login button
    username_input = browser.find_element(By.XPATH, "//*[@id='username']")
    password_input = browser.find_element(By.ID, "password")
    login_button = browser.find_element(By.ID, "submit")
    username_input.send_keys(os.getenv('USER_NAME'))
    password_input.send_keys(os.getenv('USER_PASSWORD'))
    
    login_button.click()
    
    
    # The program will wait until the success message is visible 
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='loop-container']/div/article/div[1]/h1"))
    )
    
    # Returns the browser after logging inside the web application
    yield browser

    # This will log you out from the website 
    logout_button = browser.find_element(By.XPATH, "//a[@class='wp-block-button__link has-text-color has-background has-very-dark-gray-background-color']")
    logout_button.click()

# Testing successful login test cases
def test_login_successful(login):
    # Verify that the user is successfully logged in by checking for a specific element
    success_message = login.find_element(By.XPATH,"//div[@class='post-header']/h1[@class='post-title']")
    assert "Logged In Successfully" in success_message.text