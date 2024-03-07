import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv


load_dotenv()


@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def login(browser):
    
    # Open the web application in a browser
    browser.get(os.getenv('URL'))

    # Enter valid credentials (username and password) and submit the login form
    username_input = browser.find_element(By.XPATH, "//*[@id='username']")
    password_input = browser.find_element(By.ID, "password")
    login_button = browser.find_element(By.ID, "submit")
    username_input.send_keys(os.getenv('USER_NAME'))
    password_input.send_keys(os.getenv('USER_PASSWORD'))
    
    login_button.click()
    
    
    # Wait for the page to load after login
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='post-header']/h1[@class='post-title']"))
    )
    
    # Return the browser instance after logging in
    yield browser

    # Perform cleanup actions
    logout_button = browser.find_element(By.XPATH, "//a[@class='wp-block-button__link has-text-color has-background has-very-dark-gray-background-color']")
    logout_button.click()

def test_login_successful(login):
    # Verify that the user is successfully logged in by checking for a specific element or page title
    welcome_message = login.find_element(By.XPATH,"//div[@class='post-header']/h1[@class='post-title']")
    assert "Logged In Successfully" in welcome_message.text
