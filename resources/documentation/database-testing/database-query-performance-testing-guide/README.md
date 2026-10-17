# Database Query Performance Testing Companion

Diagnostic SQL queries and a runnable sysbench load script for the [Database Query Performance Testing Guide](https://qapractices.com/documentation/database-query-performance-testing-guide/) on QAPractices.

## Contents

| File | What it does |
|---|---|
| `sql/pg-diagnostics.sql` | PostgreSQL diagnostic pack: top queries by cumulative time (pg_stat_statements), unused indexes, lock waits, buffer hit ratio. |
| `sql/explain-orders.sql` | The EXPLAIN ANALYZE example from the guide — spot a missing index on a user-orders lookup. |
| `sysbench/oltp-shop-test.sh` | sysbench 1.0+ OLTP read/write workload against a staging database (prepare + run + cleanup). |

## Usage

```bash
# Diagnostics — run against your staging PostgreSQL
psql -h db-staging.acme-shop.internal -U qa_user -d shop_db -f sql/pg-diagnostics.sql

# Missing-index example (seed orders first, then compare plans before/after the index)
psql -h db-staging.acme-shop.internal -U qa_user -d shop_db -f sql/explain-orders.sql

# OLTP load test — edit host/credentials first
bash sysbench/oltp-shop-test.sh
```

## Notes

- `pg-diagnostics.sql` requires `pg_stat_statements` enabled (`shared_preload_libraries = 'pg_stat_statements'`).
- Set `DB_HOST`, `DB_USER`, `DB_PASS`, `DB_NAME` env vars before running the sysbench script.
- Always run load scripts against staging, never production.
