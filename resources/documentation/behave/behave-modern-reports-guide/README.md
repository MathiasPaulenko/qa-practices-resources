# Payment Reports — Behave Modern Reports Demo

This is a minimal Behave project that shows how to generate multiple report formats from a single suite.

## What it contains

- `features/payment.feature` — two simple payment scenarios.
- `features/steps/payment_steps.py` — matching step definitions.
- `behave.ini` — all modern report formatters pre-registered.
- `pyproject.toml` — optional extras for each report package.
- `environment.py` — environment hooks.

## Install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[ci]"
mkdir -p reports
```

## Run a report

```bash
# Markdown
behave -f markdown -o reports/report.md

# JSON
behave -f modern-json -o reports/report.json

# HTML
behave -f modern-html -o reports/report.html

# CSV
behave -f csv -o reports/report.csv

# XLSX
behave -f xlsx -o reports/report.xlsx

# TXT
behave -f modern-txt -o reports/report.txt

# Console (on Windows set PYTHONIOENCODING=utf-8)
behave -f modern-console
```

## Windows console note

If the console formatter fails with a `UnicodeEncodeError`, set `PYTHONIOENCODING=utf-8` before running:

```powershell
$env:PYTHONIOENCODING = "utf-8"
behave -f modern-console
```

## Full guide

See the [QAPractices guide](https://qapractices.com/documentation/behave-modern-reports-guide) for setup, CI examples, debugging and decision tables.
