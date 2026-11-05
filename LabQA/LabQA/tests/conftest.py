import os
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.getenv('LABQA_URL', 'http://127.0.0.1:8000').rstrip('/')

@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--window-size=1280,900')
    if os.getenv('HEADLESS', '0') == '1':
        options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)
    driver.get(BASE_URL + '/index.html')
    driver.execute_script('localStorage.clear()')
    driver.refresh()
    yield driver
    driver.quit()

@pytest.fixture
def wait(browser):
    return WebDriverWait(browser, 10)
