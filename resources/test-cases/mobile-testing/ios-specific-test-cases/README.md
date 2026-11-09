# iOS-Specific Test Cases — Companion Files

Assets for [iOS-Specific Test Cases: 30 Scenarios](https://qapractices.com/test-cases/ios-specific-test-cases/).

## Contents

| File | Purpose |
|---|---|
| `src/appium-ios-caps.py` | Appium 2.x `XCUITestOptions` capabilities for Simulator and real-device runs, with a background/foreground state check (TC-001). |
| `src/LifecycleTests.swift` | XCUITest specs for lifecycle and permission cases: state preservation (TC-001), interruption monitor for permission alerts (TC-005/006), and Universal Link launch (TC-026). |
| `src/apns-payloads.json` | APNs payload fixtures for the notification cases: alert push, silent push (TC-004), badge decrement (TC-011), and time-sensitive interruption level (TC-012). |

## Usage

```bash
pip install "Appium-Python-Client>=4.0"
# Start the Appium 2.x server with the XCUITest driver installed, then:
python src/appium-ios-caps.py
```

Update `BUNDLE_ID` and `UDID` for your app and device before running. For the Swift specs, drop `LifecycleTests.swift` into your app's UI test target in Xcode 15+.

Send the APNs fixtures to a device with `xcrun simctl push <device> <bundleId> <payload>.json` (Simulator) or via a push-testing tool such as the `pushtry` CLI for real devices.
