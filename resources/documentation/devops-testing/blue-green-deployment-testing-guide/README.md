# Blue-Green Deployment Testing — Companion Kit

Runnable scripts for each testing phase of a blue-green deployment, companion to the [Blue-Green Deployment Testing Guide](https://qapractices.com/documentation/blue-green-deployment-testing-guide).

## Contents

| File | Purpose |
|---|---|
| `green_gate.sh` | Pre-switch readiness gate: polls green health endpoints until all answer 200 or the attempt budget runs out. |
| `rollout.yaml` | Argo Rollouts 1.7 `blueGreen` strategy with preview service, manual promote gate and 5-minute blue warm window. |
| `smoke_test.py` | Post-switch smoke test: checks core user journeys on green and fails fast on any non-2xx. |
| `metric_gate.py` | Compares green metrics against the blue baseline and outputs promote/rollback. |
| `rollback_drill.py` | Rollback drill: writes a marker on green, verifies it's readable on blue after the switch (catches schema drift). |
| `metrics_baseline.json` / `metrics_green_sample.json` | Example metric snapshots for the gate. |
| `test_metric_gate.py` | pytest suite for the metric gate logic. |

## Requirements

- Bash + curl for `green_gate.sh` (Linux/macOS/WSL/Git Bash).
- Python 3.10+, stdlib only. `pytest` for the test suite.
- `kubectl` + Argo Rollouts 1.7 to apply `rollout.yaml` on a real cluster.

## Usage

```bash
# 1. Pre-switch: block until green is ready
GREEN_URL=https://green.internal ./green_gate.sh

# 2. Switch traffic (load balancer, ingress or Argo Rollouts promote)

# 3. Post-switch: smoke test the live color
TARGET_URL=https://app.internal python smoke_test.py

# 4. Metric gate: promote or rollback
python metric_gate.py metrics_baseline.json metrics_green_sample.json
# exit 0 -> promote green, exit 1 -> rollback to blue

# 5. Rollback drill (needs the two /drill/* debug routes described in the file)
BLUE_URL=http://localhost:8081 GREEN_URL=http://localhost:8082 python rollback_drill.py
```

## Tests

```bash
python -m pytest test_metric_gate.py -v
```

## Metric thresholds

`metric_gate.py` compares each metric against a limit expressed as:

- `abs` — absolute delta (used for `error_rate`, where relative deltas on tiny rates are meaningless). Default: +0.001 (0.1 percentage point).
- `rel` — relative delta over baseline. Defaults: p99 latency +20%, CPU +15%, memory +10%.

Tune `THRESHOLDS` to your own baselines — the defaults are example values from the guide, not universal numbers.
