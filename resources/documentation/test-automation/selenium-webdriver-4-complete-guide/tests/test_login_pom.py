"""Login flow through a Page Object Model — mirrors Step 4 of the guide."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.url)
        return self

    def enter_email(self, email):
        self.wait.until(EC.visibility_of_element_located((By.ID, "email"))).send_keys(email)
        return self

    def enter_password(self, password):
        self.driver.find_element(By.ID, "password").send_keys(password)
        return self

    def click_login(self):
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='login-button']"))).click()
        return self

    def error_message(self):
        # the <p> is always "visible" (min-height) — wait for text, not visibility
        self.wait.until(EC.text_to_be_present_in_element((By.ID, "error-message"), "Invalid"))
        return self.driver.find_element(By.ID, "error-message").text

    def is_at_dashboard(self):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='welcome-msg']"))).is_displayed()


def test_successful_login(driver, app_url):
    page = LoginPage(driver, app_url)
    page.open().enter_email("qa.tester@acme-store.io").enter_password("secretpassword").click_login()
    assert page.is_at_dashboard()


def test_failed_login_shows_error(driver, app_url):
    page = LoginPage(driver, app_url)
    page.open().enter_email("qa.tester@acme-store.io").enter_password("wrongpassword").click_login()
    assert "Invalid credentials" in page.error_message()
