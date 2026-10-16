"""Selenium 4 features: relative locators, explicit waits, windows, alerts."""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.ui import WebDriverWait


def test_relative_locator_finds_password_above_login_button(driver, app_url):
    driver.get(app_url)
    login_button = driver.find_element(By.ID, "login-btn")
    password = driver.find_element(locate_with(By.TAG_NAME, "input").above(login_button))
    assert password.get_attribute("id") == "password"


def test_explicit_wait_for_delayed_element(driver, app_url):
    driver.get(app_url)
    btn = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "delayed-btn"))
    )
    assert btn.is_displayed()


def test_spinner_disappears_after_login(driver, app_url):
    driver.get(app_url)
    driver.find_element(By.ID, "email").send_keys("qa.tester@acme-store.io")
    driver.find_element(By.ID, "password").send_keys("secretpassword")
    driver.find_element(By.ID, "login-btn").click()
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.ID, "loading-spinner"))
    )


def test_new_tab_window_handle(driver, app_url):
    driver.get(app_url)
    main_handle = driver.current_window_handle
    driver.find_element(By.ID, "open-tab").click()
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
    new_handle = [h for h in driver.window_handles if h != main_handle][0]
    driver.switch_to.window(new_handle)
    driver.close()
    driver.switch_to.window(main_handle)
    assert driver.current_window_handle == main_handle


def test_confirm_alert_accept(driver, app_url):
    driver.get(app_url)
    driver.find_element(By.ID, "confirm-btn").click()
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    assert "Delete item" in alert.text
    alert.accept()
