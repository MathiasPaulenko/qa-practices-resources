import pytest
from pages.login_page import LoginPage
from utils.test_data_loader import TestDataLoader

@pytest.mark.smoke
@pytest.mark.parallel
class TestLogin:

    def test_valid_login(self, driver, base_url):
        login_page = LoginPage(driver, base_url)
        login_page.load()

        user = TestDataLoader.get_user("standard")
        login_page.login(user["username"], TestDataLoader.get_password("standard"))

        assert login_page.get_success_message() is not None
        assert "secure area" in login_page.get_success_message().lower()

    def test_invalid_password(self, driver, base_url):
        login_page = LoginPage(driver, base_url)
        login_page.load()

        user = TestDataLoader.get_user("standard")
        login_page.login(user["username"], "wrongpassword")

        error = login_page.get_error_message()
        assert error is not None, "No error message displayed"
        assert "invalid" in error.lower()

    def test_empty_credentials(self, driver, base_url):
        login_page = LoginPage(driver, base_url)
        login_page.load()

        login_page.login("", "")

        error = login_page.get_error_message()
        assert error is not None, "No validation error for empty fields"

@pytest.mark.regression
class TestLoginNavigation:

    def test_login_page_loads(self, driver, base_url):
        login_page = LoginPage(driver, base_url)
        login_page.load()

        assert login_page.is_loaded(), "Login page did not load correctly"
