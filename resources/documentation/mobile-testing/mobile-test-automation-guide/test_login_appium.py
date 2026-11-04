"""Login flow test with Appium (UiAutomator2).

Same scenario as login-flow.yaml: enter credentials, sign in,
assert the home greeting. Uses accessibility-id selectors, which
survive localization and layout changes better than text or XPath.
"""

import pytest


@pytest.fixture
def driver():
    """Provide a driver session — wire your Appium client here."""
    pytest.skip("requires a configured Appium session")


def test_login(driver):
    driver.find_element(
        "-android uiautomator",
        'new UiSelector().description("login-email")',
    ).send_keys("qa@company.com")
    driver.find_element("accessibility id", "login-password").send_keys(
        "correct-horse"
    )
    driver.find_element("accessibility id", "login-submit").click()

    greeting = driver.find_element("accessibility id", "home-greeting")
    assert greeting.is_displayed()
