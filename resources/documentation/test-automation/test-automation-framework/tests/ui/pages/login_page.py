# tests/ui/pages/login_page.py
from playwright.sync_api import Page

from core.config import Config


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(f"{Config.BASE_URL}/login")

    def login(self, email: str, password: str):
        self.page.get_by_test_id("email-input").fill(email)
        self.page.get_by_test_id("password-input").fill(password)
        self.page.get_by_test_id("login-button").click()

    def error_message(self):
        return self.page.locator("[data-testid='login-error']").text_content()
