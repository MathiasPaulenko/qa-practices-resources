# Appium Mobile Testing Tutorial — Companion Repo

> Companion repository for the [Appium Mobile Testing Tutorial: iOS & Android](https://qapractices.com/documentation/appium-mobile-testing-tutorial) on QAPractices.com.

## What's inside

- **Java test examples** for Appium 2 with iOS and Android
- **Capability files** for emulator, real device, and CI configurations
- **GitHub Actions workflow** for Android emulator CI/CD

## Stack

| Tool | Version |
| --- | --- |
| Appium Server | 2.0.0 |
| Appium Java Client | 9.2.0 |
| Selenium Java | 4.21.0 |
| JUnit Jupiter | 5.10.2 |
| Java | 17+ |

## Project structure

```text
appium-mobile-testing-tutorial/
├── pom.xml
├── .github/workflows/
│   └── appium-android-tests.yml
├── src/test/java/com/shop/qa/
│   ├── AndroidLoginTest.java
│   ├── GestureExamplesTest.java
│   ├── ExplicitWaitTest.java
│   └── IOSPredicateExampleTest.java
└── src/test/resources/capabilities/
    ├── android-emulator.json
    ├── android-real-device.json
    ├── ios-simulator.json
    └── ios-real-device.json
```

## Running the tests

### Prerequisites

1. Install Appium Server 2: `npm install -g appium@2.0.0`
2. Install drivers: `appium driver install uiautomator2` and `appium driver install xcuitest`
3. Start Appium: `appium`
4. Android Studio with an emulator running (for Android tests)
5. Xcode with iOS Simulator (for iOS tests, macOS only)

### Run all tests

```bash
mvn test
```

### Run a specific test class

```bash
mvn test -Dtest=AndroidLoginTest
mvn test -Dtest=GestureExamplesTest
mvn test -Dtest=ExplicitWaitTest
mvn test -Dtest=IOSPredicateExampleTest
```

## Capability files

Capability files are in `src/test/resources/capabilities/`. Replace `/path/to/app.apk` and `/path/to/app.app` with real paths to your app builds.

| File | Use case |
| --- | --- |
| `android-emulator.json` | Android emulator (Pixel 7, API 34) |
| `android-real-device.json` | Android physical device (set `udid`) |
| `ios-simulator.json` | iOS Simulator (iPhone 15, iOS 17.5) |
| `ios-real-device.json` | iOS physical device (set `udid` and signing) |

## CI/CD

The GitHub Actions workflow in `.github/workflows/appium-android-tests.yml` runs Android tests on API levels 30 and 34 using the `reactivecircus/android-emulator-runner` action.

## Related resources

- [Appium Mobile Testing Tutorial](https://qapractices.com/documentation/appium-mobile-testing-tutorial)
- [Appium vs Espresso vs XCUITest](https://qapractices.com/documentation/appium-vs-espresso-vs-xcuitest)
- [Mobile App Testing Checklist](https://qapractices.com/checklists/mobile-app-testing-checklist)
- [Appium Test Script Template](https://qapractices.com/templates/appium-test-script-template)

## License

MIT
