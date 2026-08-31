# HIL Testing Guide — Companion

Runnable pytest framework for HIL testing: HilRig abstraction, fault injection test, conftest fixtures and CI workflow for the [HIL Testing Guide](https://qapractices.com/documentation/hardware-in-the-loop-testing/).

## Contents

| File | What it does |
| --- | --- |
| `hil_rig.py` | HilRig class that wraps the real-time simulator (dSPACE, NI, OPAL-RT) |
| `dut_interface.py` | DutInterface class that talks to the DUT over CAN |
| `conftest.py` | pytest fixtures for rig setup/teardown |
| `test_hil_motor.py` | Example test: overcurrent protection with fault injection |
| `.github/workflows/hil-tests.yml` | GitHub Actions workflow for scheduled HIL regression |

## Quick Start

```bash
# 1. Install dependencies
pip install pytest python-can

# 2. Configure your rig URL and CAN bus
export HIL_SIMULATOR_URL="dspace://hil-rig-01"
export HIL_CAN_BUS="vcan0"
export HIL_DUT_NODE_ID="0x12"

# 3. Run the HIL test suite
pytest test_hil_motor.py -v

# 4. Run with trace recording
pytest test_hil_motor.py -v --hil-traces=./traces
```

## CI

The `.github/workflows/hil-tests.yml` file runs the HIL smoke suite on a schedule (nightly) and on demand. HIL tests need a physical rig, so they can't run on every commit — the workflow uses `workflow_dispatch` and `schedule` triggers.

## License

MIT — see the main repository for details.
