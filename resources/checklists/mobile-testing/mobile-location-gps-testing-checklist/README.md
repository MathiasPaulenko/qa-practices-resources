# Mobile Location & GPS Testing Checklist Companion

Companion resource for the [Mobile Location & GPS Checklist](https://qapractices.com/checklists/mobile-location-gps-testing-checklist). Contains mock-location scripts for the Android emulator and real devices, plus a permission flow test skeleton.

## Files

| File | Purpose |
|------|---------|
| `mock_location.sh` | Send a mock GPS fix to an Android emulator via `geo fix`, or enable mock location on a real device with `adb` |
| `test_location_permission_flow.py` | Permission flow test: trigger the system dialog, grant permission, assert the feature works |

## Quick Start

```bash
# Emulator (first emulator listens on 5554)
./mock_location.sh emulator 37.4219983 -122.084

# Real device with developer options + mock-location app configured
./mock_location.sh device 37.4219983 -122.084

python -m pytest test_location_permission_flow.py -v
```

## Requirements

- Android SDK platform-tools (`adb`, emulator telnet console)
- Python 3.11+ with pytest 8.x and an Appium or UI test driver for the flow test
- For iOS: use Xcode's simulated location or a `.gpx` file instead — mock location is not available outside the simulator

## Notes

- `geo fix` sets a static coordinate; script a series of fixes to simulate a route, or use the emulator's route playback.
- Detect mock providers in tests with `Location.isFromMockProvider()` (API 31+) or `ALLOW_MOCK_LOCATION` on older APIs.
- The permission test asserts on `com.android.packageinstaller` IDs — adjust for your target Android version; permission dialog IDs differ across OEM skins.
