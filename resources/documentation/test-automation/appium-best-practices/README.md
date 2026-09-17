# Appium Best Practices — Companion

Runnable companion for the [Appium Best Practices guide](https://qapractices.com/documentation/appium-best-practices). Contains a working driver factory, a page object example, capability presets, and a GitHub Actions job that runs the tests on an Android emulator.

## Files

| File | Purpose |
| ---- | ------- |
| `capabilities/android-emulator.json` | UiAutomator2 preset for a Pixel 7 API 34 emulator |
| `capabilities/ios-simulator.json` | XCUITest preset for an iPhone 15 simulator |
| `pages/login_screen.py` | Page object: locators and intent methods in one place |
| `tests/conftest.py` | Driver factory + screenshot/page-source capture on failure |
| `tests/test_login_flow.py` | Two example tests using the page object |
| `requirements.txt` | `Appium-Python-Client` 4.x, pytest 8.x, Selenium 4.x |
| `.github/workflows/appium-android.yml` | CI job: Appium 2 + UiAutomator2 + Android emulator |

## Requirements

- Node.js 20+ and `appium@2` (`npm install -g appium@2`)
- Appium drivers: `appium driver install uiautomator2 xcuitest`
- Python 3.11+ with `pip install -r requirements.txt`
- An Android emulator or iOS simulator with the app under test installed,
  or a device farm (BrowserStack, Sauce Labs) endpoint in `APPIUM_URL`

## Usage

```bash
# Start the Appium server
appium -p 4723

# Run the example tests against an Android emulator
CAPS_FILE=capabilities/android-emulator.json pytest tests/ -v

# iOS simulator
CAPS_FILE=capabilities/ios-simulator.json pytest tests/ -v
```

On failure, `tests/conftest.py` writes `artifacts/{test}.png` and `artifacts/{test}-page.xml` so every red test ships its own evidence.
