# SQL Test Cases — Companion

Runnable materials for the [SQL Test Cases: UrbanThreads E-Commerce Example](https://qapractices.com/test-cases/sql-test-cases/) resource on QAPractices.

## Contents

| File | What it is |
|---|---|
| `seed.sql` | UrbanThreads schema and sample data in MySQL 8.x dialect: `customers`, `products`, `inventory`, `orders`, `order_items`, `transactions`, `store_credit`, `users`, `order_audit`, plus the Alice/Bob/Carol rows and `retro-denim-jacket` with `stock_count = 10`. |
| `sp_create_order.sql` | `sp_CreateOrder` stored procedure used by TC-006: validates input first, then creates the order, decrements stock and writes the audit row inside one transaction. |
| `test_queries.sql` | The queries behind TC-001 through TC-007 as a commented script: SELECT checks, injection payloads, the rollback demo, keyset pagination, `sp_CreateOrder` calls and `EXPLAIN` runs. |

## Quick start

```bash
# Load the schema and sample data (MySQL 8.x client)
mysql -u qa -h staging.db.urbanthreads.com -D urbanthreads < seed.sql

# Create the stored procedure used by TC-006
mysql -u qa -h staging.db.urbanthreads.com -D urbanthreads < sp_create_order.sql

# Run the test queries (comment/uncomment the destructive lines as needed)
mysql -u qa -h staging.db.urbanthreads.com -D urbanthreads < test_queries.sql
```

For PostgreSQL 16, replace `ENUM` with `VARCHAR` plus a `CHECK` constraint and `AUTO_INCREMENT` with `GENERATED ALWAYS AS IDENTITY`; the queries themselves are dialect-neutral except `CALL`/`LIMIT`, which work in both engines.

## Notes

- `test_queries.sql` is intentionally conservative: destructive statements (the forced FK violation, the invalid `sp_CreateOrder` calls, `CREATE`/`DROP INDEX`) are commented out so a full-file run is read-only.
- The concurrency scenario in TC-004 needs two separate client sessions — run the Session A and Session B blocks from different terminals. `information_schema.innodb_trx` (MySQL) or `pg_locks` (PostgreSQL) shows which transaction is waiting.
- `transactions` ships with only the columns the suite uses; to reproduce the deep-pagination timing, generate the 10M-row volume yourself instead of seeding it here.
