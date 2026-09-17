"""Page object for the login screen.

Locators live here, not in test code. Tests call intent methods
(login, assert_error_visible) instead of touching elements directly.
"""

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginScreen:
    EMAIL = (AppiumBy.ACCESSIBILITY_ID, "email-field")
    PASSWORD = (AppiumBy.ACCESSIBILITY_ID, "password-field")
    SUBMIT = (AppiumBy.ACCESSIBILITY_ID, "login-button")
    ERROR = (AppiumBy.ACCESSIBILITY_ID, "login-error")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout, poll_frequency=0.5)

    def login(self, user: str, password: str) -> None:
        self.wait.until(EC.element_to_be_clickable(self.EMAIL)).send_keys(user)
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.SUBMIT).click()

    def error_visible(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self.ERROR))
            return True
        except Exception:
            return False
