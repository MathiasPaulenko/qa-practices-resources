import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

APPIUM_SERVER = "http://localhost:4723"

CAPABILITIES = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "emulator-5554",
    # Replace with your APK path — fixture intentionally left empty.
    "appium:app": "",
    "appium:noReset": False,
}


@pytest.fixture()
def driver():
    """Start an Appium session; requires a running appium server + emulator."""
    if not CAPABILITIES["appium:app"]:
        pytest.skip("Set CAPABILITIES['appium:app'] to your APK path")
    drv = webdriver.Remote(APPIUM_SERVER, options=UiAutomator2Options().load_capabilities(CAPABILITIES))
    yield drv
    drv.quit()
