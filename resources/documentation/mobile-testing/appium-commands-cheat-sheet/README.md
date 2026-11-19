# Appium Commands Cheat Sheet — Companion Repo

> Companion repository for the [Appium Commands Cheat Sheet](https://qapractices.com/documentation/appium-commands-cheat-sheet) on QAPractices.com.

## What's inside

- **`AppiumCommandsExamples.java`** — a compilable class that mirrors every code section of the cheat sheet: driver setup, locators, `mobile:` gestures, W3C Actions, app/device commands and waits.

## Stack

| Tool | Version |
| --- | --- |
| Appium Server | 2.x |
| Appium Java Client | 9.2.0 |
| Selenium Java | 4.21.0 |
| Java | 17+ |

## Usage

The class is a reference, not a runnable suite — each method maps to a section of the cheat sheet and assumes a live session against an Appium server.

```bash
# Start the server (Appium 2.x serves on "/", no /wd/hub)
npm install -g appium
appium driver install uiautomator2
appium

# Compile the examples
mvn compile
```

To run any snippet for real, point the capabilities at your app and emulator/device, then call the method you need from a JUnit test.

## Notes on Appium 2.x

- Server URL is `http://localhost:4723` — no `/wd/hub` suffix.
- `launchApp`, `closeApp`, `resetApp` were removed in java-client 8+; use `activateApp`/`terminateApp` and the `noReset`/`fullReset` capabilities.
- UiAutomator2 `swipeGesture` and `scrollGesture` require a `direction` parameter.
- The tap-on-coordinates gesture is `mobile: clickGesture` — `mobile: tap` does not exist on UiAutomator2 (it exists on XCUITest with different parameters).
