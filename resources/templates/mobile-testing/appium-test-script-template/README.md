# Appium Test Script Template — Companion

Runnable files for the [Appium Test Script Template](https://qapractices.com/templates/appium-test-script-template/) on QAPractices. Copy the skeleton into your project, fill the TODO markers and run it against a local Appium 2.x server — no copy-paste from the browser needed.

## Files

| File | What it is |
|---|---|
| `appium-test-template.js` | The blank skeleton: environment config, W3C capabilities for UiAutomator2 (with the XCUITest variant commented), session setup, explicit-wait helper, test flow and teardown |
| `appium-login-sample.js` | The same skeleton completed for a login flow on a fictional e-commerce Android app (`shopwave-2.4.1-debug.apk`, `Pixel_8_API_34` emulator) |

## Usage

1. Install Appium 2.x and the drivers: `npm i -g appium`, then `appium driver install uiautomator2` (and `xcuitest` on macOS for iOS).
2. Add WebdriverIO to your project (`npm i webdriverio`) or port the file to your test runner of choice.
3. Fill every TODO marker in `appium-test-template.js`: app path, device name, accessibility IDs, expected text.
4. Start the server (`appium` listens on `http://127.0.0.1:4723` by default) and run the script.

## Related

- [Appium Test Script Template](https://qapractices.com/templates/appium-test-script-template/) — the full template with best practices, common mistakes and FAQ
- [Appium Commands Cheat Sheet](https://qapractices.com/documentation/appium-commands-cheat-sheet/) — the driver commands used inside the flow blocks
