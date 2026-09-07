from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get("https://staging.qa.local/login")

    def login(self, email, password):
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "[data-testid='login-button']").click()
        self.wait.until(EC.url_contains("/dashboard"))

    def get_error_message(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.ID, "error"))
        ).text
