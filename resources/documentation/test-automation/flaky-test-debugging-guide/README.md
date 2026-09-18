# Flaky Test Debugging Guide — Companion

Companion resource for [Flaky Test Debugging Guide: A Systematic Approach](https://qapractices.com/documentation/flaky-test-debugging-guide).

Runnable pytest project demonstrating the detection workflow from the guide's triage section: loop runs with pytest-repeat, order shuffling with pytest-randomly, and a quarantine marker that keeps flaky tests out of the blocking suite without losing them.

## Contents

- `tests/test_stable.py` — deterministic control tests (`stable` marker)
- `tests/test_counter_flaky.py` — counter-driven flakiness: fails every 3rd run, so `--count=6` always marks 2 iterations as `R` (rerun)
- `tests/test_order_dependency.py` — shared-state pair that only fails when `pytest-randomly` runs it in the wrong order
- `tests/test_quarantined.py` — quarantined test excluded from the blocking suite (`quarantined` marker)
- `pytest.ini` — marker registration
- `requirements.txt` — pytest 8.4.1, pytest-repeat 0.9.4, pytest-randomly 3.16.0, pytest-rerunfailures 15.1

## Requirements

- Python 3.10+
- `pip install -r requirements.txt`

## Usage

```bash
# The green blocking suite — everything that isn't flaky or quarantined
pytest -m "not flaky and not quarantined"

# Detection loop: rerun the counter test 6 times — 2 iterations show as R
pytest tests/test_counter_flaky.py --count=6

# Order dependency: shuffle until test_b lands before test_a
pytest tests/test_order_dependency.py
# note the --randomly-seed printed in the header to replay a failing order

# Quarantine suite: check on tests under investigation
pytest -m quarantined
```

## What each run teaches

- **`--count=N`** (pytest-repeat) measures failure rate — intermittent failure means flakiness, consistent failure means a real bug.
- **`pytest-randomly`** shuffles order automatically; if tests only fail under shuffling you have shared state, not timing.
- **Markers as quarantine** keep flaky tests visible (still tracked, still runnable) without letting them block the pipeline — the workflow from the guide's Prevention Strategies.

See the guide for root-cause categories, the symptom-to-fix triage matrix, and the five debugging techniques.
