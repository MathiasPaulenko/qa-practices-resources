# XCUITest Guide for iOS UI Testing — Companion

Companion files for the [XCUITest Guide for iOS UI Testing](https://qapractices.com/documentation/xcuitest-guide-ios-testing).

## Files

| File | Purpose |
| --- | --- |
| `tests/LoginPage.swift` | Page Object Model for the login screen with accessibility identifiers. |
| `tests/LoginTests.swift` | Login success and failure tests using the Page Object Model. |
| `tests/QueryExamples.swift` | Element query examples: by identifier, text, index, children, firstMatch. |
| `.github/workflows/xcuitest-ios.yml` | GitHub Actions workflow for running XCUITest on macOS runners. |

## Requirements

- macOS with Xcode 15.4+
- iOS Simulator (iPhone 15 or iPhone SE 3rd generation)
- Swift 5.9+
- An iOS project with accessibility identifiers set on UI elements

## Usage

1. Copy the `tests/` directory into your `MyAppUITests/` folder.
2. Update the `accessibilityIdentifier` values to match your app.
3. Copy the GitHub Actions workflow to `.github/workflows/`.
4. Update the `xcodebuild` command with your project name and scheme.
5. Run `xcodebuild test -project MyApp.xcodeproj -scheme MyApp -destination "platform=iOS Simulator,name=iPhone 15"`.

## CI Integration

The workflow runs XCUITest on two simulators (iPhone 15 and iPhone SE 3rd generation) in parallel. Adjust the matrix for your needs.
