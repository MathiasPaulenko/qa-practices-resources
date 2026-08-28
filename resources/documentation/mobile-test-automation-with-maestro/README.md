# Mobile Test Automation with Maestro — Companion

Companion project for [Mobile Test Automation with Maestro: iOS & Android](https://qapractices.com/documentation/mobile-test-automation-with-maestro/).

## Requirements

- Maestro CLI 2.8.0
- Java 11+
- Node.js 20 LTS (for CI)
- Xcode (for iOS simulator) or Android Studio (for Android emulator)

## Install Maestro

```bash
curl -Ls "https://get.maestro.mobile.dev" | bash
export PATH="$PATH:$HOME/.maestro/bin"
maestro --version
```

## Files

| File | Purpose |
| --- | --- |
| `flows/home-screen.yaml` | Basic launch + search flow |
| `flows/profile-flow.yaml` | Login subflow + profile navigation |
| `flows/checkout-flow.yaml` | Conditional logic for empty cart + checkout |
| `subflows/login.yaml` | Reusable login subflow with env vars |
| `.github/workflows/mobile-tests.yml` | GitHub Actions CI workflow for macOS simulator |

## Run a Flow

```bash
maestro test flows/home-screen.yaml
```

## Run All Flows

```bash
maestro test flows/
```

## Run with Environment Variables

```bash
EMAIL="qa-tester@qapractices.test" PASSWORD="TestPass123!" maestro test flows/profile-flow.yaml
```

## CI Integration

The included GitHub Actions workflow runs all flows on `macos-latest` with an iPhone 15 simulator. It uploads screenshots and logs as artifacts on failure.

## Related Resource

- [Mobile Test Automation with Maestro](https://qapractices.com/documentation/mobile-test-automation-with-maestro/)
- [Appium Mobile Testing Tutorial](https://qapractices.com/documentation/appium-mobile-testing-tutorial/)
- [Mobile App Testing Checklist](https://qapractices.com/checklists/mobile-app-testing-checklist/)
