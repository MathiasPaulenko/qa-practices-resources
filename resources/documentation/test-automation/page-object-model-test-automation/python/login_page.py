from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.email = (By.ID, "email")
        self.password = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
        self.error_message = (By.CSS_SELECTOR, ".error-message")

    def navigate_to(self):
        # Placeholder: replace with your environment URL
        self.driver.get("https://staging.qapractices.com/login")

    def enter_email(self, email):
        element = self.wait.until(EC.visibility_of_element_located(self.email))
        element.clear()
        element.send_keys(email)

    def enter_password(self, password):
        element = self.driver.find_element(*self.password)
        element.clear()
        element.send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.login_button).click()

    def login(self, email, password):
        from dashboard_page import DashboardPage
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        return DashboardPage(self.driver)

    def get_error_message(self):
        element = self.wait.until(EC.visibility_of_element_located(self.error_message))
        return element.text
