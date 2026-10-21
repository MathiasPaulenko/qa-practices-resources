# Data Quality Validation Rules Template — Runnable Companion

Companion for [Data Quality Validation Rules Template](https://qapractices.com/templates/data-quality-validation-rules-template/) / [versión en español](https://qapractices.com/es/templates/data-quality-validation-rules-template/).

`dq_runner.py` runs the eight check types from the register — completeness, uniqueness, format, range, referential integrity, consistency, business rules — against an in-memory SQLite dataset, plus a min-rows load gate and a weighted DQ score. `seed(clean=False)` loads a dataset with one defect per check type so every rule can be observed firing; `seed(clean=True)` produces the all-green baseline.

## Run

```bash
python dq_runner.py      # prints PASS/WARN/FAIL per check + dimension scores
python -m unittest discover tests -v
```

Requirements: Python 3.9+, standard library only.

## What each check maps to

| Runner check | Template section |
|---|---|
| `check_min_rows` | 1.3 record count / zero-row load gate |
| `check_completeness` | 1.2 null and missing value checks |
| `check_uniqueness` | 2.1-2.2 PK and natural-key duplicates |
| `check_format` | 3.1-3.3 patterns, types, enums |
| `check_range` | 4.1-4.3 numeric/date boundaries |
| `check_referential` | 5.1-5.2 FK orphans |
| `check_consistency` | 6.1 cross-field rules (paid vs amount paid) |
| `check_business_rules` | 7.1 custom rules (customs form, cancel reason) |
| `run_all` score | 7.3 weighted DQ score |

The seeded run reports an overall score of 25.0 with failures across every dimension — that's intentional: the point of the sample is to see each check fire, not to look healthy.
