# Mobile Testing Guide — Companion

Runnable companion for the [Mobile App Testing Guide](https://qapractices.com/documentation/mobile-testing-guide/) on QAPractices.

Implements the two pieces that don't fit in an article: a device matrix you can fill from your analytics, and the smoke-test commands for both platforms.

## Files

- `device-matrix.csv` — Tier 1/2/3 device selection template: model, OS version, audience share, owner, test cadence. Replace the sample rows with your top devices from analytics.
- `run-smoke-tests.sh` — smoke runner for both stacks: Espresso on an Android emulator and XCUITest on an iOS simulator, with env vars for the test class/scheme.

## Run

```bash
# Android (needs an emulator running or a connected device)
./run-smoke-tests.sh android

# iOS (needs a booted simulator)
./run-smoke-tests.sh ios
```

Requires an Android project with `connectedDebugAndroidTest` set up or an Xcode scheme with UI tests — see the guide for what belongs in a smoke suite.
