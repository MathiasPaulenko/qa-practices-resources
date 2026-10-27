# Database Testing Queries — SQLite fixture

Companion for [AI Prompts for Database Testing Query Generation](https://qapractices.com/prompts/ai-prompt-database-testing-queries/).

The `users`/`orders`/`order_items` schema from the resource, with the generated test queries made runnable. The inserts marked `-- must FAIL` are negative cases: they *should* raise constraint errors. All `SELECT` checks should return 0 rows.

## Run

```bash
sqlite3 test_db.sqlite "PRAGMA foreign_keys = ON;"
sqlite3 test_db.sqlite < schema.sql
sqlite3 test_db.sqlite < test-queries.sql   # expect constraint errors on marked inserts
```

Note: sqlite enforces FKs only with `PRAGMA foreign_keys = ON` — itself a classic setup bug this fixture demonstrates.
