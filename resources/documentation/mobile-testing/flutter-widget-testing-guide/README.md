# Flutter Widget Testing — Companion

Companion resource for [Flutter Widget Testing: 4 Layers with Dart Examples](https://qapractices.com/documentation/flutter-widget-testing-guide).

## Contents

- `lib/utils/validators.dart` — Email validator used in unit test examples
- `lib/widgets/login_button.dart` — LoginButton widget used in widget and golden tests
- `test/utils/validators_test.dart` — Unit test example (Layer 1)
- `test/widgets/login_button_test.dart` — Widget test example (Layer 2)
- `test/golden/login_button_golden_test.dart` — Golden file test example (Layer 4)
- `integration_test/login_flow_test.dart` — Integration test example (Layer 3)
- `test/helpers/mock_api_service.dart` — Mockito mock generation helper
- `pubspec.yaml` — Dependencies with pinned versions

## Requirements

- Flutter SDK 3.24.0+
- Dart 3.5.0+

## Usage

```bash
# Install dependencies
flutter pub get

# Run unit and widget tests
flutter test

# Generate mocks
dart run build_runner build

# Run integration tests (requires emulator or device)
flutter test integration_test/

# Update golden baselines
flutter test --update-goldens
```

## Versions

- Flutter: 3.24.0
- Mockito: 5.4.4
- build_runner: 2.4.15
