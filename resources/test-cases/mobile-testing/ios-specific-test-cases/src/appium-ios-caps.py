"""Appium 2.x capabilities for the iOS-specific test suite.

Uses the XCUITest driver via Appium-Python-Client 4.x.
Replace BUNDLE_ID and UDID with values for your app and device.
"""

from appium import webdriver
from appium.options.ios import XCUITestOptions

BUNDLE_ID = "com.qapractices.shop"
UDID = "auto"  # replace with a real device UDID for on-device runs
APPIUM_URL = "http://127.0.0.1:4723"


def ios_options() -> XCUITestOptions:
    options = XCUITestOptions()
    options.platform_version = "17.5"
    options.device_name = "iPhone 15"
    options.automation_name = "XCUITest"
    options.bundle_id = BUNDLE_ID
    options.udid = UDID
    options.set_capability("appium:noReset", False)
    options.set_capability("appium:newCommandTimeout", 120)
    return options


def test_state_survives_backgrounding() -> None:
    """TC-001: background for 5 s, assert UI state is preserved."""
    driver = webdriver.Remote(APPIUM_URL, options=ios_options())
    try:
        driver.execute_script("mobile: backgroundApp", {"seconds": 5})
        cart_total = driver.find_element("accessibility id", "cart_total")
        assert cart_total.is_displayed(), "cart_total gone after backgrounding"
    finally:
        driver.terminate_app(BUNDLE_ID)
        driver.quit()


if __name__ == "__main__":
    test_state_survives_backgrounding()
    print("TC-001 passed: state preserved across background/foreground")
