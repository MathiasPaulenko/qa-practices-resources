# Risk-Based Testing — Companion Resources

Artifacts matching the examples in [Risk-Based Testing: A Practical Approach](https://qapractices.com/documentation/risk-based-testing/).

## Contents

| File | Purpose |
|---|---|
| `src/risk-register.csv` | Risk register template: area, likelihood (1-5), impact (1-5), score, priority, mitigation tests, owner. Prefilled with the e-commerce example from the guide. |
| `src/pytest.ini` | Marker registration for `critical`, `high`, `medium`, `low` so `pytest -m` filtering works without warnings. |
| `src/test_risk_markers.py` | Example tests tagged with risk markers, matching the CI pipeline from the guide. |
| `src/risk-report-template.md` | The risk-level test summary table + open risks block, ready to paste into a release report. |

## Usage

```bash
# Run only critical and high-risk tests
pytest -m "critical or high"

# Deep-risk pass before release
pytest -m "critical" --count 3   # requires pytest-repeat
```

Scoring convention: `Risk Level = Likelihood x Impact`, both rated 1-5. Scores of 15+ map to Critical, 8-14 High, 4-7 Medium, below 4 Low — adjust thresholds to your context.
