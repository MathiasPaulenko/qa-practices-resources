# Mobile App Test Cases — Companion Files

Assets for [Mobile App Test Cases: Practical QA Test Cases for Teams](https://qapractices.com/test-cases/mobile-app-test-cases/).

## Contents

| File | Purpose |
|---|---|
| `src/desired-caps.py` | Appium-Python-Client 4.x capability sets for Android (UiAutomator2) and iOS (XCUITest), using the modern `AppiumOptions` API — no deprecated `find_element_by_accessibility_id`. |
| `src/device-coverage-matrix.csv` | Device × OS coverage matrix for the suite: which group of test cases runs on which tier (real device, emulator, device farm). |

## Usage

```bash
pip install Appium-Python-Client>=4.0
# Start the Appium 2.x server locally, then:
python src/desired-caps.py
```

Update `APP_PACKAGE` / `BUNDLE_ID` and `UDID` for your app and device before running.
