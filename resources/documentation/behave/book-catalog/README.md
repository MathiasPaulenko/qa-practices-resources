# Behave BDD Book Catalog Example

A complete, runnable Behave example for the [Behave BDD Project Setup Guide](https://qapractices.com/documentation/behave-bdd-project-setup-guide/).

This project shows the same catalog under three different testing layers:

1. **In-memory catalog** — direct Python unit-style BDD.
2. **HTTP API catalog** — a small `http.server` and a `requests` client.
3. **SQLite catalog** — database-backed BDD with savepoint rollback.

## Run

```bash
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate on Windows
pip install -r requirements-dev.txt
```

### Run all features

```bash
behave
```

### Run only one layer

```bash
# In-memory catalog
behave --tags='~api' --tags='~db'

# HTTP API
behave --tags=api

# SQLite
behave --tags=db
```

### CI-friendly reports

```bash
mkdir -p reports
behave --junit --junit-directory=reports/junit --format=json --outfile=reports/behave-report.json
```

## Project structure

```text
book-catalog/
├── catalog_service.py           # in-memory catalog
├── catalog_db.py                # SQLite catalog
├── book_server.py               # HTTP server for the API
├── api_client.py                # requests wrapper
├── behave.ini                   # configuration and userdata
├── requirements-dev.txt
├── pyproject.toml
└── features/
    ├── environment.py           # unified hooks for all three layers
    ├── book_catalog.feature     # in-memory scenarios
    ├── book_api.feature         # API scenarios
    ├── book_catalog_db.feature  # SQLite scenarios
    └── steps/
        ├── book_catalog_steps.py     # steps for in-memory and SQLite
        └── api_steps.py         # steps for the API
```

## Tags

- `@smoke` — quick, representative scenarios.
- `@regression` — extended coverage.
- `@api` — HTTP API scenarios.
- `@db` — SQLite scenarios.
- `@integration` — switch `context.base_url` to `REAL_API_URL` from `behave.ini`.
