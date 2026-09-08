# iOS App Testing Checklist — Companion

> Companion resource for [iOS App Testing Checklist](https://qapractices.com/checklists/ios-app-testing-checklist) on QAPractices.com.

XCUITest login test and Appium iOS capabilities for the iOS App Testing Checklist.

## Requirements

- Xcode 15+ with XCTest and XCUITest
- Appium 2.x with the XCUITest driver
- Python 3.10+ (for Appium scripts)
- iOS Simulator or a physical iOS device

## Setup

```bash
# XCUITest (Swift)
# 1. Open the .xcodeproj in Xcode
# 2. Select a simulator or connected device
# 3. Run the LoginTests target with Cmd+U

# Appium (Python)
pip install Appium-Python-Client
appium driver install xcuitest
appium --use-plugins=images
python appium/ios_login_test.py
```

## Files

| File | Purpose |
| ---- | ------- |
| `tests/LoginTests.swift` | XCUITest login test with valid and invalid credentials |
| `appium/ios_login_test.py` | Appium iOS login test with XCUITest driver |
| `appium/capabilities.py` | Reusable Appium capabilities for iOS |

## License

MIT — free to use, modify, and distribute. Never store production credentials in test config; always use environment variables or sandbox accounts.
