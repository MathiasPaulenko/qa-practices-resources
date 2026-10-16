import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

APP_URL = (Path(__file__).resolve().parent.parent / "app" / "login.html").as_uri()


@pytest.fixture
def driver():
    options = Options()
    if os.getenv("SELENIUM_HEADLESS", "true").lower() == "true":
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    d = webdriver.Chrome(options=options)
    d.implicitly_wait(0)
    yield d
    d.quit()


@pytest.fixture
def app_url():
    return APP_URL
