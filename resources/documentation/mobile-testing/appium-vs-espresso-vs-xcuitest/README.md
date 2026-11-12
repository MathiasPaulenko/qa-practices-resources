# Appium vs Espresso vs XCUITest Companion

Companion resource for [Appium vs Espresso vs XCUITest: Native iOS & Android](https://qapractices.com/documentation/appium-vs-espresso-vs-xcuitest). The same login scenario implemented once per framework so you can compare syntax, setup and execution model side by side.

## Files

| File | Framework | Execution model |
|------|-----------|-----------------|
| `AppiumLoginTest.java` | Appium 2.x + UiAutomator2, `appium-java-client` 9.x | Out-of-process, HTTP/WebDriver |
| `LoginEspressoTest.kt` | Espresso 3.5+ (AndroidX Test 1.5+) | In-process, `androidTest` source set |
| `LoginUITest.swift` | XCUITest, Xcode 15+ | Separate runner process, accessibility APIs |

## Quick Start

```bash
# Appium (server + uiautomator2 driver installed, app on device/emulator)
appium &                    # Appium Server 2.x listens on :4723
javac AppiumLoginTest.java  # needs appium-java-client 9.x on the classpath

# Espresso (inside the app's androidTest source set)
./gradlew connectedAndroidTest

# XCUITest (macOS + Xcode required)
xcodebuild test -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 16'
```

## Requirements

- Appium Server 2.x with the `uiautomator2` driver (`appium driver install uiautomator2`)
- `appium-java-client` 9.x for the Java example
- Android SDK + emulator or device for Espresso
- macOS + Xcode 15+ for XCUITest

## Notes

- Replace `com.example.app`, the `R.id.*` selectors and the `accessibilityIdentifier` keys with your app's real identifiers. Accessibility IDs survive localization and layout changes better than text or XPath.
- The same login flow takes roughly 2-5 s under Appium (HTTP round-trips) versus under a second in Espresso (in-process) — the speed gap the article explains.
- `qa@staging.acme.dev` is a placeholder: use a dedicated test account on your staging environment.
