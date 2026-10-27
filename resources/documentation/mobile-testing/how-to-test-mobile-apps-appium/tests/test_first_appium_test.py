"""First Appium test — mirrors Steps 3-7 of the guide.

Requires: appium server on :4723, an Android emulator, and an APK path set in
conftest.py. Runs as a skip (not fail) when the APK is not configured.
"""
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_home_screen_loads(driver):
    wait = WebDriverWait(driver, 15)
    title = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//*[contains(@text, 'Home')]")
    ))
    assert title.is_displayed()


def test_element_by_accessibility_id(driver):
    wait = WebDriverWait(driver, 15)
    button = wait.until(EC.presence_of_element_located(
        (AppiumBy.ACCESSIBILITY_ID, "login-button")
    ))
    assert button.is_enabled()


def test_element_by_resource_id(driver):
    wait = WebDriverWait(driver, 15)
    field = wait.until(EC.presence_of_element_located(
        (AppiumBy.ID, "com.example.app:id/username")
    ))
    assert field.is_displayed()
