# How to Perform Database Testing with SQL — Companion

Runnable pytest project for the [How to Perform Database Testing with SQL](https://qapractices.com/documentation/how-to-perform-database-testing-sql) guide on QAPractices.

## What it covers

- `tests/test_crud.py` — INSERT/UPDATE verification with `RETURNING id`
- `tests/test_constraints.py` — UNIQUE, NOT NULL and FOREIGN KEY violations asserting `psycopg2.IntegrityError`
- `tests/test_transactions.py` — rollback behavior and `ON DELETE CASCADE` integrity
- `tests/conftest.py` — `db_connection` and `seeded_users` fixtures with automatic schema setup/teardown

## Requirements

- Python 3.10+
- A dedicated PostgreSQL instance (Docker recommended): `docker run -e POSTGRES_PASSWORD=test -e POSTGRES_USER=test -e POSTGRES_DB=testdb -p 5432:5432 postgres:16`
- Never point this at production — the fixture uses env vars (`DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`) with placeholder defaults.

## Run

```bash
pip install -r requirements.txt
pytest -v
```
