"""Login flow example using the page object and explicit waits.

Requires: Appium server 2.x running (appium -p 4723), UiAutomator2
driver installed, and the app under test at the path in the caps JSON.
"""

from pages.login_screen import LoginScreen


def test_login_with_valid_credentials(driver):
    login = LoginScreen(driver)
    login.login("qa@qapractices.dev", "correct-horse-battery")
    assert not login.error_visible()


def test_login_rejects_wrong_password(driver):
    login = LoginScreen(driver)
    login.login("qa@qapractices.dev", "wrong-password")
    assert login.error_visible()
