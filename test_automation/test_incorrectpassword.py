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
def student(browser):
    # Gets the URL and opens the website in browser
    browser.get(os.getenv('URL'))
    return browser  

# Test cases for unsuccessful login by passing incorrect password
def test_incorrect_password(student):
    username_input = student.find_element(By.XPATH, "//*[@id='username']")
    password_input = student.find_element(By.ID, "password")
    submit_button = student.find_element(By.ID, "submit")
    username_input.clear()
    username_input.send_keys(os.getenv('USER_NAME'))
    password_input.clear()
    # Fetching the username from env and concatenating incorrect password
    password_input.send_keys(os.getenv('USER_PASSWORD')+"incorrectPassword")
    submit_button.click()
    error_message = WebDriverWait(student, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='error']")))
    assert error_message.text == 'Your password is invalid!'