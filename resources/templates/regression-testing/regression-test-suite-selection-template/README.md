# Regression Test Suite Selection — Companion Scorer

Companion for the QAPractices resource
[Regression Test Suite Selection Template](https://qapractices.com/templates/regression-test-suite-selection-template/).

`regression_selector.py` implements the template's weighted scoring model:

```
Score = BC*0.30 + DH*0.25 + CI*0.20 + AU*0.15 + ET*0.10
```

Each of `bc`, `dh`, `ci`, `au`, `et` is rated 0-3:

| Column | Criterion | Weight |
|---|---|---|
| `bc` | Business criticality | 30% |
| `dh` | Defect history | 25% |
| `ci` | Code change impact | 20% |
| `au` | Automation status | 15% |
| `et` | Execution time | 10% |

The weighted score assigns the tier:

| Score | Tier |
|---|---|
| 2.50 – 3.00 | T0 Smoke |
| 2.00 – 2.49 | T1 Core |
| 1.50 – 1.99 | T2 Full |
| 0.00 – 1.49 | T3 Change-specific |

## Usage

```bash
pip install -r requirements.txt
python regression_selector.py test_cases.csv selection_plan.csv
```

Output:

```text
T0:2 T1:3 T2:3 T3:2  (10 total)
```

`selection_plan.csv` lists each test sorted by weighted score with its tier.
`test_cases.csv` mirrors the numbers used in the template's Completed Sample.

## Tests

```bash
pytest -v
```
