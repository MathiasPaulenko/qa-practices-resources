import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Placeholder URL — replace with your app's login page
LOGIN_URL = "https://example.com/login"


class TestLogin:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get(LOGIN_URL)

    def teardown_method(self, method):
        self.driver.quit()

    def login(self, email, password):
        self.driver.find_element(By.ID, "email").clear()
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()

    def test_successful_login(self):
        self.login("test@test.com", "Test123!")
        self.wait.until(EC.url_contains("/dashboard"))
        assert self.driver.find_element(By.ID, "dashboard").is_displayed()

    @pytest.mark.parametrize(
        "email,password,expected",
        [
            ("test@test.com", "wrongpass", "Invalid credentials"),
            ("", "Test123!", "Email is required"),
            ("test@test.com", "", "Password is required"),
            ("invalid", "Test123!", "Please enter a valid email"),
        ],
    )
    def test_invalid_login(self, email, password, expected):
        self.login(email, password)
        error = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".error-message"))
        )
        assert error.text == expected
