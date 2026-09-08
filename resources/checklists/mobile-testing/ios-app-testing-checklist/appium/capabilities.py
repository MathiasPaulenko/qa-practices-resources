# appium/capabilities.py
"""Reusable Appium capabilities for iOS testing."""

from appium import webdriver


def get_ios_capabilities(app_path: str, device_name: str = "iPhone 15") -> dict:
    """Return capabilities for an iOS Simulator run.

    Args:
        app_path: Absolute path to the .app bundle built for the simulator.
        device_name: Simulator device name (must exist in `xcrun simctl list`).
    """
    return {
        "platformName": "iOS",
        "platformVersion": "17.0",
        "deviceName": device_name,
        "automationName": "XCUITest",
        "app": app_path,
        "udid": "auto",
    }


def create_driver(app_path: str, server_url: str = "http://127.0.0.1:4723"):
    """Create an Appium driver with iOS capabilities."""
    caps = get_ios_capabilities(app_path)
    return webdriver.Remote(server_url, desired_capabilities=caps)
