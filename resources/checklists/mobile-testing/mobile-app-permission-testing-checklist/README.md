# Mobile App Permission Testing Checklist Companion

Companion resource for the [Mobile App Permission Testing Checklist](https://qapractices.com/checklists/mobile-app-permission-testing-checklist). Contains an `adb` helper script for granting, revoking, resetting, and inspecting Android runtime permissions, plus an Appium/WebdriverIO test skeleton for the main permission flows.

## Files

| File | Purpose |
|------|---------|
| `permission_adb.sh` | Grant, revoke, reset, or dump runtime permissions for a package on a connected Android device or emulator |
| `appium_permissions.test.js` | Appium WebdriverIO test skeleton: auto-grant flow, permanent denial routing to Settings, and iOS one-shot alert handling |

## Quick Start

```bash
# Grant camera permission to the installed build
./permission_adb.sh com.example.app grant android.permission.CAMERA

# Revoke it and relaunch to test the denial path
./permission_adb.sh com.example.app revoke android.permission.CAMERA

# Restore all runtime permissions to install state
./permission_adb.sh com.example.app reset

# Inspect the current grant state of every declared permission
./permission_adb.sh com.example.app dump

# Run the Appium skeleton (edit capabilities first)
node appium_permissions.test.js
```

## Requirements

- Android SDK platform-tools (`adb`) for the shell script.
- Node.js 20+ with `webdriverio` and an Appium 2.x server with the `uiautomator2` and `xcuitest` drivers.
- For iOS denial-flow tests on a simulator, `xcrun simctl privacy <device> reset <bundleId>` resets all privacy grants between runs.

## Notes

- `autoGrantPermissions` skips the system dialog entirely — use it for happy-path suites only, never when the denial flow itself is under test.
- Permission dialog element IDs (`com.android.packageinstaller`) vary across Android versions and OEM skins; assert on your app's own UI for the settings deep link.
- Android 11+ can auto-reset permissions for unused apps. Simulate the re-request path by revoking with `pm revoke` and relaunching instead of waiting for the system job.
