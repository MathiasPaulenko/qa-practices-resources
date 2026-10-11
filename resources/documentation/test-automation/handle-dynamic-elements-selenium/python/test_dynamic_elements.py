"""Runnable examples from "How to Handle Dynamic Web Elements in Selenium"
(Selenium 4.25+, Chrome). Runs against local HTML fixtures — no network needed.
ChromeDriver must be on PATH or managed via Selenium Manager.

Usage: python -m pytest -v
"""
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


@pytest.fixture()
def driver():
    options = Options()
    options.add_argument("--headless=new")
    d = webdriver.Chrome(options=options)
    yield d
    d.quit()


def test_dynamic_id_locate_by_stable_testid_and_wait_clickable(driver):
    driver.get((FIXTURES / "dynamic-page.html").as_uri())
    wait = WebDriverWait(driver, 10)

    # The button ID is regenerated on every load — data-testid is stable.
    button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "[data-testid='save-button']")))
    # Fallback without data-testid: match the stable ID prefix.
    fallback = driver.find_element(By.CSS_SELECTOR, "button[id^='btn_']")

    assert button.is_displayed()
    assert fallback.is_displayed()


def test_ajax_content_wait_for_spinner_then_results(driver):
    driver.get((FIXTURES / "dynamic-page.html").as_uri())
    wait = WebDriverWait(driver, 10)

    wait.until(EC.invisibility_of_element_located((By.ID, "spinner")))
    wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, ".search-result")))

    assert len(driver.find_elements(By.CSS_SELECTOR, ".search-result")) == 5


def test_dynamic_dropdown_click_then_wait_for_options(driver):
    driver.get((FIXTURES / "dynamic-page.html").as_uri())
    wait = WebDriverWait(driver, 10)

    driver.find_element(By.ID, "dropdown-trigger").click()
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, ".dropdown-option")))

    options = driver.find_elements(By.CSS_SELECTOR, ".dropdown-option")
    chosen = [o for o in options if o.text == "Desired Option"]
    assert chosen
    chosen[0].click()


def test_shadow_dom_native_get_shadow_root(driver):
    driver.get((FIXTURES / "dynamic-page.html").as_uri())

    # Selenium 4 native shadow DOM support.
    host = driver.find_element(By.CSS_SELECTOR, "#shadow-host")
    shadow_root = host.shadow_root

    assert shadow_root.find_element(
        By.CSS_SELECTOR, "#shadow-button").is_displayed()


def test_custom_wait_element_gets_active_class(driver):
    driver.get((FIXTURES / "dynamic-page.html").as_uri())
    wait = WebDriverWait(driver, 10)

    def element_has_class(d, locator, class_name):
        element = d.find_element(*locator)
        return class_name in (element.get_attribute("class") or "")

    wait.until(lambda d: element_has_class(d, (By.ID, "status"), "active"))
    assert driver.find_element(By.ID, "status").text == "Ready"


def test_iframe_switch_in_interact_and_switch_back(driver):
    driver.get((FIXTURES / "iframe-page.html").as_uri())

    driver.switch_to.frame("inner-frame")
    driver.find_element(By.ID, "inside-frame").send_keys("text")
    assert driver.find_element(By.ID, "inside-button").is_displayed()

    # Forget this and every find_element below runs in the wrong context.
    driver.switch_to.default_content()
    assert driver.find_element(By.TAG_NAME, "h1").is_displayed()
