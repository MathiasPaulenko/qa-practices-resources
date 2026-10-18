# CSV Import Test Lab

Runnable companion for [CSV and Excel Import Test Cases](https://qapractices.com/test-cases/csv-excel-import-test-cases/) — a stdlib-only Python importer that exercises the failure modes from the suite: delimiter sniffing, BOM handling, header normalization, row-level errors, duplicates, partial vs atomic import, and formula-injection sanitization.

## Run

```bash
pip install -r requirements.txt
pytest -v
```

## What it covers

| Test | Suite case |
|---|---|
| `test_valid_file_imports_all_rows` | TC001 happy path |
| `test_semicolon_delimiter_rejected` | TC002 wrong delimiter |
| `test_utf8_bom_does_not_corrupt_first_header` | TC003 BOM |
| `test_missing_email_reports_exact_row` | TC005 row-level errors |
| `test_invalid_email_rejected_by_row` | TC005/TC006 field validation |
| `test_duplicate_email_second_occurrence_flagged` | TC007 duplicates |
| `test_header_variants_map_to_canonical` | TC008 header mapping |
| `test_quoted_commas_and_newlines_stay_one_row` | TC009 RFC 4180 |
| `test_blank_rows_skipped_not_errors` | Edge: trailing blanks |
| `test_atomic_mode_rolls_back_everything` | TC012 rollback |
| `test_partial_mode_keeps_valid_rows` | TC012 partial import |
| `test_formula_injection_neutralized` | TC013 CSV injection |
| `test_renamed_xlsx_rejected_by_magic_bytes` | TC014 fake extension |
| `test_summary_counts_match_reality` | TC015 honest summary |
