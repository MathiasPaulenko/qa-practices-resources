# Mobile Test Automation Guide Companion

Companion resource for [Mobile Test Automation: A Practical Guide](https://qapractices.com/documentation/mobile-test-automation-guide). Contains a runnable Maestro flow and an Appium test covering the same login scenario.

## Files

| File | Purpose |
|------|---------|
| `login-flow.yaml` | Maestro flow: launch, enter credentials, sign in, assert the home greeting |
| `test_login_appium.py` | Same flow as an Appium Python test using accessibility-id selectors |

## Quick Start

```bash
# Maestro (needs a running emulator or connected device)
maestro test login-flow.yaml

# Appium (needs appium server + driver configured in conftest)
python -m pytest test_login_appium.py -v
```

## Requirements

- Maestro CLI 1.39+ for the YAML flow
- Appium 2.x with the UiAutomator2 driver for the Python test
- A debug/release build of the app under test installed on emulator or device

## Notes

- Replace `com.example.app` and the accessibility IDs with your app's real identifiers. Accessibility IDs survive localization and layout changes better than text or XPath selectors.
- Run tests against a **release build** — debug builds carry the Metro bundler and dev menus that change timing.
- Add `clearAppState` (Maestro) or a state-reset hook (Appium `beforeEach`) between scenarios so tests don't leak navigation history.
