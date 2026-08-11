# Behave CI/CD Pipeline Example

This folder contains a runnable **Behave** project that mirrors the CI/CD pipeline example from the QAPractices guide [Behave CI/CD Pipeline Guide](https://qapractices.com/documentation/behave-cicd-pipeline-guide/).

It is a small `book-catalog` service with a GitHub Actions workflow that runs the suite on Python 3.11, 3.12 and 3.13, produces JUnit XML and JSON reports, and uploads artifacts even when the job fails.

## Project structure

```text
book-catalog/
├── .github/
│   └── workflows/
│       └── behave.yml
├── behave.ini
├── pyproject.toml
├── requirements-dev.txt
├── catalog_service.py
├── discover_features.py
├── features/
│   ├── environment.py
│   ├── catalog.feature
│   └── steps/
│       └── catalog_steps.py
└── reports/
    └── .gitkeep
```

## What it demonstrates

- `catalog_service.py` is a tiny in-memory catalog used by the BDD suite.
- `features/catalog.feature` contains a `@smoke` scenario.
- `features/steps/catalog_steps.py` maps the Gherkin steps to Python.
- `features/environment.py` initializes `context.catalog` before each scenario and reads `base_url` from `behave.ini` `userdata`.
- `behave.ini` turns off color, writes `reports/behave-report.json` and `reports/junit/*.xml`, and excludes `@skip` and `@manual` tags.
- `.github/workflows/behave.yml` is the GitHub Actions matrix workflow with `if: always()` on artifact upload.
- `discover_features.py` is the shard-discovery script used in the parallel execution example.
- `pyproject.toml` and `requirements-dev.txt` pin the same dependencies.

## Run locally

```bash
cd book-catalog
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
mkdir -p reports
behave
```

Expected output:

```text
Feature: Catalog search

  @smoke
  Scenario: Find a book by title
    Given the catalog contains "Clean Code"
    When I search for "Clean Code"
    Then I should find 1 book

1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
3 steps passed, 0 failed, 0 skipped
```

After the run, `reports/` contains:

- `behave-report.json` — pretty-printed JSON report.
- `junit/TESTS-catalog.xml` — JUnit XML for CI dashboards.

## Run with behavex

```bash
behavex --parallel-processes=4 --parallel-scheme=feature
```

## Discover feature shards

```bash
python discover_features.py
```
