"""Pytest fixtures for deep link test cases.

Requires Appium 2.5, pytest 8.3 and an Appium server running locally.
"""

import pytest
from appium import webdriver
from deep_link_utils import trigger_android_deep_link, trigger_ios_deep_link


@pytest.fixture
def android_driver():
    """Create an Android Appium driver for deep link testing."""
    caps = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "appPackage": "com.qapractices.shop",
        "appActivity": ".MainActivity",
        "noReset": True,
    }
    driver = webdriver.Remote("http://localhost:4723", caps)
    yield driver
    driver.quit()


@pytest.fixture
def ios_driver():
    """Create an iOS Appium driver for deep link testing."""
    caps = {
        "platformName": "iOS",
        "automationName": "XCUITest",
        "bundleId": "com.qapractices.shop",
        "noReset": True,
    }
    driver = webdriver.Remote("http://localhost:4723", caps)
    yield driver
    driver.quit()


@pytest.fixture
def deep_link_url():
    """Default deep link URL for testing."""
    return "https://shop.qapractices.com/product/123"
