# How to Test AI-Powered Features — Companion

Companion files for the [How to Test AI-Powered Features guide](https://qapractices.com/documentation/how-to-test-ai-powered-features).

## Files

| File | Purpose |
| --- | --- |
| `tests/golden-dataset.json` | Curated golden dataset with 2 sentiment examples (expand to 50-200 for production). |
| `tests/test_model_contract.py` | Contract test: schema, status code, latency, confidence range. |
| `tests/test_sentiment_behavior.py` | Property-based assertions: label in expected range, confidence above minimum. |
| `tests/test_model_drift.py` | Drift detection: computes F1 on golden dataset and blocks deploy below baseline. |
| `tests/test_shadow_comparison.py` | Shadow test: compares current vs candidate model on same input. |
| `tests/test_adversarial_robustness.py` | Adversarial robustness: empty, gibberish, long, ambiguous, non-English, contradictory. |

## Requirements

- Python 3.10+
- pytest 8.3+
- requests 2.32+

## Usage

1. Copy the `tests/` directory to your project.
2. Update the `BASE_URL` in each test file to point to your staging API.
3. Expand `golden-dataset.json` with 50-200 representative inputs.
4. Run `pytest tests/ -v` to execute all tests.
5. On first run, generate baselines for F1 and confidence thresholds.
6. Block deploys when drift tests fail.

## CI Integration

```yaml
- run: pytest tests/ -v --tb=short
```
