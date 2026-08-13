# behave-tables Example — User Access Report

This folder contains a runnable **Behave** project that accompanies the QAPractices guide [Behave Tables Made Easy](https://qapractices.com/documentation/behave-tables-guide/).

It demonstrates how to wrap Behave data tables with `behave-tables`, convert rows to dicts, compare tables, and export to CSV with `behave-tables==1.3.1` and `behave==1.3.3` on Python 3.11+.

## Project structure

```text
user_access_report/
├── .github/workflows/behave-tables.yml
├── behave.ini
├── pyproject.toml
├── requirements.txt
├── access_service.py
└── features/
    ├── environment.py
    ├── access_report.feature
    └── steps/
        └── access_steps.py
```

`access_service.py` is a tiny in-memory service used by the BDD suite. `features/steps/access_steps.py` uses `behave-tables` to convert, filter, compare, and export table data.

## Run locally

```bash
cd user_access_report
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
behave --no-capture
```

Expected output:

```text
Feature: User access report

  @smoke
  Scenario: Active engineering users
    Given the system has the following users
    When I list the active users in the "eng" department
    Then I should see the following report

  @regression
  Scenario: Export the report as CSV
    Given the system has the following users
    When I export the report as CSV
    Then the CSV output should contain 2 active users

1 feature passed, 0 failed, 0 skipped
2 scenarios passed, 0 failed, 0 skipped
7 steps passed, 0 failed, 0 skipped
```
