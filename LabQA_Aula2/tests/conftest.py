import os
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.getenv("LABQA_URL", "http://127.0.0.1:8000").rstrip("/")

@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1280,900")
    driver = webdriver.Chrome(options=options)
    driver.get(BASE_URL + "/login.html")
    driver.execute_script("localStorage.clear(); sessionStorage.clear();")
    yield driver
    driver.quit()

@pytest.fixture
def wait(browser):
    return WebDriverWait(browser, 10)
