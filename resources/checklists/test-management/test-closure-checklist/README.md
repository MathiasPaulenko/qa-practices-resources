# Test Closure Checklist — Companion Script and Fixtures

> Companion resource for [Test Closure Checklist](https://qapractices.com/checklists/test-closure-checklist) on QAPractices.com.

Python Test Exit Report generator, test data fixtures and CI workflow for test closure with Python 3.12 and pytest 8.3.

## Requirements

- Python 3.12+
- pytest 8.3

## Setup

```bash
# Install dependencies
pip install pytest==8.3

# Run the Test Exit Report generator
python scripts/generate_exit_report.py --release v2.1.0 --results fixtures/test_results.json --defects fixtures/open_defects.json

# Run the closure validation tests
pytest scripts/test_closure_validation.py -v

# Run the CI workflow locally
python scripts/generate_exit_report.py --release v2.1.0 --results fixtures/test_results.json --defects fixtures/open_defects.json --output reports/
```

## Files

| File | Purpose |
| ------ | --------- |
| `scripts/generate_exit_report.py` | Python script to generate a Test Exit Report from test results and open defects |
| `scripts/test_closure_validation.py` | pytest tests to validate closure checklist items (coverage, defects, artifacts) |
| `fixtures/test_results.json` | Sample test results with passed, failed and blocked statuses |
| `fixtures/open_defects.json` | Sample open defects with severity, owner and business impact |
| `.github/workflows/closure-validation.yml` | CI workflow to validate closure on every release branch push |

## Test Data

The `fixtures/` directory contains reusable test data:

- `test_results.json` — 20 test cases with mixed statuses (passed, failed, blocked)
- `open_defects.json` — 5 open defects with severity levels and business impact

## License

MIT — free to use, modify, and distribute. Never store production credentials in test fixtures; always use synthetic data.
