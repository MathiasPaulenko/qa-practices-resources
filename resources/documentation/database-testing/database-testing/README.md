# Database Testing — Integrity-Check Companion

Companion code for [Database Testing Guide](https://qapractices.com/documentation/database-testing/) on QAPractices.

## What is inside

| File | What it shows |
|------|---------------|
| `schema.sql` | Minimal e-commerce schema (users, products, orders, order_lines) with NOT NULL / UNIQUE / CHECK / FOREIGN KEY constraints — SQLite dialect, no server needed. |
| `seed.sql` | Clean seed data; every check reports 0 violations. |
| `integrity_checks.sql` | The 5 integrity checks from the guide: orphaned lines, total mismatches, duplicate emails, non-positive prices, bad quantities. Each query returns a violation count. |
| `run_checks.py` | Runs the checks against an in-memory DB or a `.db` file; prints `OK`/`FAIL` per check and exits 0/1 — drop into CI as-is. |
| `tests/test_integrity.py` | 10 pytest cases: clean seed passes everything, tampered data (orphan, drifted total, duplicate email, negative price) is caught, `PRAGMA foreign_keys` blocks orphans at insert time. |

## Run it

```bash
python run_checks.py          # in-memory demo DB
python -m pytest tests/ -v    # the suite
```

Expected: all checks `OK` on the seed, **10 passed**.

The suite uses `sqlite3` from the stdlib — the only dependency is pytest 8.3.4. The same SQL runs on PostgreSQL/MySQL with minimal dialect changes.

## Related resource

- [Database Testing Guide](https://qapractices.com/documentation/database-testing/) — the full strategy this code implements (Steps 1–4).
