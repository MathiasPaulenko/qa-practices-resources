# Database Transactions Testing — Companion

Runnable companion for [How to Test Database Transactions and Rollbacks](https://qapractices.com/documentation/database-transactions-testing/).

Five live demos mapped to the guide's sections — each one fails loudly if transaction behavior breaks:

| Demo | What it proves |
| --- | --- |
| Atomicity | A mid-transaction failure leaves no partial write |
| Savepoint | `ROLLBACK TO SAVEPOINT` undoes later work, keeps earlier work |
| Optimistic locking | A stale `version` write is rejected (lost-update protection) |
| Implicit rollback | Disconnecting without `COMMIT` discards everything |
| Consistency | `CHECK (balance >= 0)` aborts an overdraft transfer |

## Files

| File | Purpose |
| --- | --- |
| `schema.sql` | `accounts` + `transfers` tables with CHECK/FK constraints and a `version` column for optimistic locking. |
| `seed.sql` | Two accounts, 100 each — clean starting state. |
| `transaction_demos.py` | The five demos above; run it to see each behavior pass. |
| `tests/test_transactions.py` | The same behaviors as pytest cases (7 tests). |

## Usage

```bash
python transaction_demos.py       # run the narrated demos
pip install -r requirements.txt   # pytest only
python -m pytest tests/ -v        # run as a test suite
```

Requires Python 3.8+ — `sqlite3` is stdlib, no database server needed.

## Notes

- SQLite was chosen so the demos run with zero setup. The guide's isolation-level and deadlock sections need a client-server engine — PostgreSQL or MySQL — where `SELECT FOR UPDATE`, `deadlock_timeout` and real concurrent sessions apply.
- The optimistic-locking demo is the pattern, not a substitute for your ORM's implementation (SQLAlchemy `@declared_attr` version columns, Hibernate `@Version`).
- `demo.db` is created next to the script and recreated on each run.
