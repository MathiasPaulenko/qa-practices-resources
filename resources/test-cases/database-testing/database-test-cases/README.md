# Database Test Cases — Companion

Runnable artifacts for the [Database Test Cases](https://qapractices.com/test-cases/database-test-cases) suite (35 cases over a two-table `users`/`orders` dataset).

## Files

| File | What it does |
|---|---|
| `seed.sql` | Creates the schema and fixture all 35 cases reference (PostgreSQL 12+). |
| `validate.sql` | Post-migration checks: constraint listing, orphan rows, NULLs, negative totals. |
| `test_injection.py` | pytest suite proving the parameterized-query pattern resists the classic `' OR '1'='1` payload — runs on in-memory SQLite, no server needed. |

## Usage

```bash
# Seed a staging database
psql -d staging_db -f seed.sql

# Post-migration validation
psql -d staging_db -f validate.sql

# Injection check (pytest 8.3+, Python 3.10+)
pip install pytest
pytest test_injection.py -v
```

The Python test uses SQLite in memory so it runs anywhere. On PostgreSQL the same principle applies: bind parameters, never interpolate user input into SQL strings.

Back to the guide: [qapractices.com/test-cases/database-test-cases](https://qapractices.com/test-cases/database-test-cases)
