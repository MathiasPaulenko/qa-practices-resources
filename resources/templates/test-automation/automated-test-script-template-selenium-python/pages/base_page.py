import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, driver, base_url="", timeout=10):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def open(self, path):
        url = f"{self.base_url}{path}" if path.startswith("/") else path
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        element = self.find_clickable(locator)
        element.click()
        logger.info(f"Clicked element: {locator}")

    def type_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        logger.info(f"Typed text into: {locator}")

    def get_text(self, locator):
        element = self.find_element(locator)
        return element.text

    def is_visible(self, locator):
        try:
            self.find_element(locator)
            return True
        except TimeoutException:
            return False

    def wait_for_element(self, locator, condition="visible"):
        conditions = {
            "visible": EC.visibility_of_element_located,
            "clickable": EC.element_to_be_clickable,
            "present": EC.presence_of_element_located,
        }
        return self.wait.until(conditions[condition](locator))

    def select_dropdown(self, locator, value):
        from selenium.webdriver.support.ui import Select
        dropdown = Select(self.find_element(locator))
        dropdown.select_by_visible_text(value)
        logger.info(f"Selected dropdown value: {value}")

    def take_screenshot(self, name):
        path = f"reports/screenshots/{name}.png"
        self.driver.save_screenshot(path)
        logger.info(f"Screenshot saved: {path}")
        return path
