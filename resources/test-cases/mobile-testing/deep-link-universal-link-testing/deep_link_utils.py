"""Deep link test utilities for Appium 2.5 + ADB 35.

Helpers to trigger deep links on iOS and Android from Appium tests.
"""

import subprocess
import platform
from typing import Optional


def trigger_android_deep_link(url: str, package: str, adb_path: str = "adb") -> str:
    """Trigger a deep link on Android via ADB 35.

    Args:
        url: The deep link URL to open.
        package: The target app package name.
        adb_path: Path to the adb binary (default: assumes adb is in PATH).

    Returns:
        The stdout from the adb command.
    """
    cmd = [
        adb_path, "shell", "am", "start", "-W",
        "-a", "android.intent.action.VIEW",
        "-d", url,
        package,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(f"ADB command failed: {result.stderr}")
    return result.stdout


def trigger_ios_deep_link(url: str) -> str:
    """Trigger a deep link on iOS Simulator via Xcode 16 simctl.

    Args:
        url: The deep link URL to open.

    Returns:
        The stdout from the simctl command.
    """
    cmd = ["xcrun", "simctl", "openurl", "booted", url]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(f"simctl command failed: {result.stderr}")
    return result.stdout


def trigger_appium_deep_link(driver, url: str, package: str, app_id: Optional[str] = None) -> None:
    """Trigger a deep link via Appium 2.5 mobile:deepLink command.

    Args:
        driver: An Appium WebDriver instance.
        url: The deep link URL.
        package: The Android package name.
        app_id: The iOS bundle ID (optional, Android only if not provided).
    """
    params = {"url": url, "package": package}
    if app_id:
        params["appId"] = app_id
    driver.execute_script("mobile:deepLink", params)
