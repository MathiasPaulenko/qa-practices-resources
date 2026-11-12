from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pages.base_page import BasePage

class DashboardPage(BasePage):
    # Locators
    WELCOME_MESSAGE = (By.CSS_SELECTOR, ".welcome-text, .flash")
    USER_MENU = (By.ID, "user-menu")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "#user-menu .logout")
    NAV_ITEMS = (By.CSS_SELECTOR, ".nav-item")
    NOTIFICATION_BADGE = (By.CSS_SELECTOR, ".notification-badge")
    SEARCH_INPUT = (By.ID, "global-search")

    def get_welcome_text(self):
        return self.get_text(self.WELCOME_MESSAGE)

    def is_loaded(self):
        return self.is_visible(self.WELCOME_MESSAGE)

    def logout(self):
        self.click(self.USER_MENU)
        self.click(self.LOGOUT_BUTTON)

    def get_notification_count(self):
        if self.is_visible(self.NOTIFICATION_BADGE):
            return self.get_text(self.NOTIFICATION_BADGE)
        return "0"

    def navigate_to(self, nav_item_text):
        items = self.driver.find_elements(*self.NAV_ITEMS)
        for item in items:
            if item.text == nav_item_text:
                item.click()
                return
        raise NoSuchElementException(f"Nav item not found: {nav_item_text}")
