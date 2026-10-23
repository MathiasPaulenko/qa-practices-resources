# CSV Import Column Mapping Test Cases — Companion

Companion resource for [CSV Import Team Member Column Mapping Test Cases](https://qapractices.com/test-cases/csv-import-column-mapping-test-cases/).

## Contents

- `csv_checks.py` — stdlib-only pre-import checks modeled on the test cases: `utf-8-sig` reading (the BOM bug from TC-019), delimiter sniffing (`,`/`;`/tab/`|`), header normalization + alias auto-mapping, required-field gating, column-count and email validation.
- `fixtures/` — real files, not generated strings: `taskflow_team.csv` (TaskFlow sample), `taskflow_utf8_bom.csv` (Excel-style BOM), `taskflow_semicolon.csv`, `taskflow_tab.tsv`, `taskflow_empty.csv`, `taskflow_headers_only.csv`, `taskflow_ragged.csv`.
- `tests/test_csv_checks.py` — 14 tests mapped to TC IDs: gate checks (empty / headers-only / bad extension), delimiter detection, quoted commas, BOM strip, whitespace trim, auto-mapping aliases, required-field blocking, ragged rows, invalid emails, duplicate emails, i18n characters.

## Requirements

- Python 3.10+, `pip install -r requirements.txt` (pytest only — checks are stdlib)

## Usage

```bash
pytest tests/ -q
```

Expected output: `14 passed`.

The UI-level cases (mapping dropdowns, preview highlight, rollback) run at browser level with Playwright 1.48 per the article's automation notes.

## Related

- Article EN: https://qapractices.com/test-cases/csv-import-column-mapping-test-cases/
- Article ES: https://qapractices.com/es/test-cases/csv-import-column-mapping-test-cases/
