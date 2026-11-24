# Regression Testing Prioritization Checklist — Companion

Executable companion for the [Regression Testing Prioritization Checklist](https://qapractices.com/checklists/regression-testing-prioritization-checklist).

## Contents

- `prioritize_tests.py` — scores every suite entry from change impact + defect history + flakiness, assigns must-run/should-run/can-skip tiers, and prints an ordered run list with the cut line drawn at your time budget.
- `sample_history.csv` — example history export format (test, area, last_failed, fails_12w, flake_rate, runtime_s).

## Usage

```bash
git diff --name-only origin/main > changed.txt
python3 prioritize_tests.py changed.txt history.csv --budget-min 60
```

Wire `changed.txt` from your diff tooling and `history.csv` from your test-management or CI results export. Feeding real defect history is what turns this from sorting into prioritization.
