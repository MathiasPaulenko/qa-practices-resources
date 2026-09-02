# Deep Link & Universal Link Test Cases — Companion

> Companion repository for [10 Deep Link & Universal Link Test Cases](https://qapractices.com/test-cases/deep-link-universal-link-testing/)

## Requirements

- Python 3.10+
- Appium 2.5
- ADB 35 (Android SDK 35)
- Xcode 16 (for iOS Simulator)
- pytest 8.3
- An Appium server running on `http://localhost:4723`
- A test app with package `com.qapractices.shop` installed on the device/emulator

## Setup

```bash
pip install pytest==8.3 appium-python-client
appium  # start the Appium server in another terminal
```

## Running the tests

```bash
# Run all tests (requires Android device/emulator)
pytest test_deep_links.py -v

# Run only the malformed link tests
pytest test_deep_links.py::TestMalformedDeepLink -v

# Run with JSON report
pytest test_deep_links.py -v --json-report
```

## Files

| File | Purpose |
| ------ | --------- |
| `deep_link_utils.py` | Helpers to trigger deep links via ADB, simctl and Appium |
| `conftest.py` | Pytest fixtures for Android and iOS Appium drivers |
| `test_deep_links.py` | Test cases TC-001 through TC-010 |
| `meta.json` | Resource metadata |

## Test coverage

| Test class | TC | Description |
| ------------ | ---- | ------------- |
| `TestDeepLinkBasic` | TC-001 | Basic deep link with app installed |
| `TestDeepLinkParameters` | TC-002 | Query and path parameter parsing |
| `TestDeepLinkAuth` | TC-004 | Authenticated screen redirect after login |
| `TestDeepLinkBackground` | TC-005 | Background resume navigation |
| `TestMalformedDeepLink` | TC-010 | Malformed link handling |
| `TestAndroidADBDirect` | TC-001/007 | Direct ADB launch without Appium |

## License

MIT — Mathias Paulenko
