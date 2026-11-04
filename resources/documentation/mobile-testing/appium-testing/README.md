# Appium Testing Guide — Companion

This companion provides runnable files for the [Appium: iOS & Android Automation](https://qapractices.com/documentation/appium-testing) guide.

## Files

| File | Purpose |
|------|---------|
| `scripts/install-drivers.sh` | Installs Appium 2.0 XCUITest and UiAutomator2 drivers, then runs `appium doctor` |
| `scripts/start-server.sh` | Starts the Appium server and verifies `/wd/hub/status` |
| `tests/login-android.wdio.js` | WebdriverIO login flow for Android (accessibility-id locators) |
| `tests/login-android.py` | Python UiAutomator2Options login flow |
| `tests/gestures.wdio.js` | swipeGesture, pinchGesture, sendBiometricMatch and deepLink examples |

## Quick Start

```bash
# Requires Node.js 18+, Android SDK (and Xcode on macOS for iOS)
npm install -g appium

bash scripts/install-drivers.sh
bash scripts/start-server.sh   # leave running, then in another terminal:

npx wdio run tests/login-android.wdio.js    # WebdriverIO test
pip install Appium-Python-Client==4.2.0
python tests/login-android.py             # Python test
```

## CI Integration

Run `install-drivers.sh` once per CI image build. Start the server in background before the test job, and run the login smoke test on an emulator before dispatching device-farm suites.
