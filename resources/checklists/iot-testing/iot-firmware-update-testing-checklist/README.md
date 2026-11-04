# IoT Firmware Update Testing Checklist Companion

Companion resource for the [IoT Firmware Update Testing Checklist](https://qapractices.com/checklists/iot-firmware-update-testing-checklist). Contains an OTA firmware manifest example and a pytest-style power-loss recovery test that exercises rollback after an interrupted update.

## Files

| File | Purpose |
|------|---------|
| `ota-manifest.json` | Example update manifest with version, minVersion, size, SHA-256 checksum and signature fields |
| `test_power_loss_recovery.py` | Power-loss recovery test: update, power cut, power restore, verify rollback version |

## Quick Start

```bash
python -m pytest test_power_loss_recovery.py -v
```

The test expects an `ota-client` CLI plus `power-cut`/`power-restore` harness commands on the PATH — swap them for your own OTA client and power-control tooling (bench supply relay, PoE switch API, or a device emulator).

## Requirements

- Python 3.11+ with pytest 8.x
- An OTA client CLI (Mender, swupdate, or your own) and a power-control harness

## Notes

- `minVersion` in the manifest is the anti-rollback floor: images below it must be rejected.
- The checksum uses SHA-256 — never MD5 or SHA-1 for firmware integrity.
- Extend the test with a health-check failure trigger to cover the watchdog rollback path.
