# Reporting & Analytics Export Testing — Companion

Companion resource for [Reporting and Analytics Export Test Cases: Data Accuracy](https://qapractices.com/test-cases/reporting-analytics-export-test-cases/).

## Contents

- `export_checks.py` — stdlib-only validators for the artifacts an export feature produces: UTF-8 BOM detection, CSV row counts excluding the header, filename sanitization (ASCII-safe, date-stamped), and parsing of the queued/completed async-export contract.
- `tests/test_export_checks.py` — pytest 8.3 suite exercising the validators against the failure modes the article covers: mojibake in Excel (TC037), row counts (TC001/TC007), filename edge cases (TC034), and the async status payload (TC033).
- `fixtures/report_q2.csv` — a BOM-prefixed CSV with non-Latin customer data.
- `fixtures/export_status_*.json` — the queued and completed payloads from the article's async example.

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
cd resources/test-cases/web-testing/reporting-analytics-export-test-cases
pytest tests/ -v
```

Quick manual check:

```bash
python export_checks.py
# BOM present: True
# Data rows: 3
# Sanitized: True
# From 'Revenue "Q2" — Café/Naïve': revenue-q2-cafe-naive
```

## What this covers

- CSV integrity: BOM, header exclusion, non-Latin round trip (TC001, TC037).
- Filename rules: ASCII-safe slugs with a date stamp (TC034).
- Async contract: `queued` → `completed` + `downloadUrl`, invalid payloads rejected (TC033).
- Boundary values in filenames: path separators, spaces, uppercase extensions.
