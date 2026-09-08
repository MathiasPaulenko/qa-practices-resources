# tests/ui/specs/test_login.py
from core.config import Config
from ui.pages.login_page import LoginPage


def test_valid_login(page):
    login = LoginPage(page)
    login.open()
    login.login("jane@qa.local", "valid-pass")
    assert page.url == f"{Config.BASE_URL}/dashboard"


def test_invalid_login(page):
    login = LoginPage(page)
    login.open()
    login.login("jane@qa.local", "wrong-pass")
    assert login.error_message() == "Invalid credentials"
