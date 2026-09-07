import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    d = webdriver.Chrome()
    d.maximize_window()
    yield d
    d.quit()


def test_successful_login(driver):
    driver.get("https://staging.qa.local/login")
    driver.find_element(By.ID, "email").send_keys("jane@qa.local")
    driver.find_element(By.ID, "password").send_keys("validpass123")
    driver.find_element(By.CSS_SELECTOR, "[data-testid='login-button']").click()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("/dashboard"))
    assert "/dashboard" in driver.current_url

    welcome = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'Welcome')]"))
    )
    assert welcome.is_displayed()
