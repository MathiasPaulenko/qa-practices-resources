"""Appium 2.x capability sets for the mobile-app-test-cases suite.

Requires Appium-Python-Client 4.x. Replace APP_PACKAGE, BUNDLE_ID and UDID
with values for your app and device.
"""
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

APPIUM_SERVER = "http://localhost:4723"
APP_PACKAGE = "com.qapractices.demo"  # Placeholder: your Android package
BUNDLE_ID = "com.qapractices.demo"  # Placeholder: your iOS bundle id
UDID = "emulator-5554"  # Placeholder: device UDID


def android_caps() -> UiAutomator2Options:
    return (
        UiAutomator2Options()
        .set_capability("platformName", "Android")
        .set_capability("appium:automationName", "UiAutomator2")
        .set_capability("appium:appPackage", APP_PACKAGE)
        .set_capability("appium:appActivity", ".MainActivity")
        .set_capability("appium:udid", UDID)
        .set_capability("appium:noReset", False)
    )


def ios_caps() -> XCUITestOptions:
    return (
        XCUITestOptions()
        .set_capability("platformName", "iOS")
        .set_capability("appium:automationName", "XCUITest")
        .set_capability("appium:bundleId", BUNDLE_ID)
        .set_capability("appium:udid", UDID)
    )


if __name__ == "__main__":
    driver = webdriver.Remote(APPIUM_SERVER, options=android_caps())
    # Modern lookup: AppiumBy instead of find_element_by_accessibility_id
    from appium.webdriver.common.appiumby import AppiumBy

    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "login").click()
    driver.quit()
