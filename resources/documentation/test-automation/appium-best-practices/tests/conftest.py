"""Driver factory + failure evidence capture.

Reads a capabilities JSON preset, starts one Appium session per test,
and saves a screenshot + page source whenever a test fails.
"""

import json
import os
from pathlib import Path

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

APPIUM_URL = os.environ.get("APPIUM_URL", "http://localhost:4723")
CAPS_FILE = os.environ.get("CAPS_FILE", "capabilities/android-emulator.json")
ARTIFACTS = Path("artifacts")


@pytest.fixture()
def driver(request):
    caps = json.loads(Path(CAPS_FILE).read_text())
    platform = caps["platformName"].lower()
    options = UiAutomator2Options() if platform == "android" else XCUITestOptions()
    options.load_capabilities(caps)

    drv = webdriver.Remote(APPIUM_URL, options=options)
    yield drv

    # Evidence on failure: screenshot + page source + (optionally) video
    if request.node.rep_call.failed:
        ARTIFACTS.mkdir(exist_ok=True)
        name = request.node.name
        drv.save_screenshot(str(ARTIFACTS / f"{name}.png"))
        (ARTIFACTS / f"{name}-page.xml").write_text(drv.page_source)
    drv.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
