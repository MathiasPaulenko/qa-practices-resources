"""Location permission flow test.

Triggers the system permission dialog from a location feature,
grants permission, and asserts the feature renders results.
Adjust the packageinstaller IDs to your target Android version.
"""

import pytest


@pytest.mark.skipif(True, reason="requires a running driver session")
def test_location_permission_flow(driver):
    driver.find_element_by_id("find-nearby").click()

    dialog = driver.find_element_by_id(
        "com.android.packageinstaller:id/permission_message"
    )
    assert "location" in dialog.text.lower()

    driver.find_element_by_id(
        "com.android.packageinstaller:id/permission_allow_button"
    ).click()

    results = driver.find_element_by_id("nearby-results")
    assert results.is_displayed()


def test_location_permission_denied_degrades(driver):
    driver.find_element_by_id("find-nearby").click()

    driver.find_element_by_id(
        "com.android.packageinstaller:id/permission_deny_button"
    ).click()

    # The app must degrade gracefully: show rationale or cached content, no crash
    degraded = driver.find_element_by_id("location-rationale")
    assert degraded.is_displayed()
