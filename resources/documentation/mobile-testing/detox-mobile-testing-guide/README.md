# Detox React Native Testing Companion

Runnable Detox v20 gray-box E2E setup for the [Detox Mobile Testing Guide](https://qapractices.com/documentation/detox-mobile-testing-guide/).

## Requirements

- Node.js 18+
- A React Native project with iOS and/or Android folders
- Xcode + CocoaPods (iOS) or Android Studio with an emulator image (Android)
- `detox-cli` installed globally: `npm install -g detox-cli`

## Files

| File | Description |
| --- | --- |
| `.detoxrc.js` | Detox v20 configuration for iOS simulator and Android emulator |
| `e2e/jest.config.js` | Jest runner setup for the E2E suite |
| `e2e/config.json` | Runner config referenced by `.detoxrc.js` |
| `e2e/login.test.js` | Login suite: valid credentials, invalid credentials, matchers, actions and assertions |
| `e2e/pages/LoginPage.js` | Page Object Model version of the same flow |
| `.github/workflows/detox.yml` | GitHub Actions workflow that builds and tests on macOS runners |

## Quick start

```bash
# inside your React Native project
npm install --save-dev detox@^20 jest
cp -r e2e .detoxrc.js /path/to/your-app/

# adjust .detoxrc.js paths to your app name and scheme
detox build -c ios
detox test -c ios
```

Replace `MyApp` in `.detoxrc.js` with your workspace/scheme name, and `Pixel_5_API_33` with an AVD that exists on your machine (`emulator -list-avds`).

## Notes

- Detox synchronizes with the app automatically — no manual sleeps needed.
- `testID` attributes must exist in your React Native components for `by.id()` matchers to find them.
- The GitHub Actions workflow needs macOS runners for iOS builds.
