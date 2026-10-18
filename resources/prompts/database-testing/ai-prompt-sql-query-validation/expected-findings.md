# Expected Findings — ai-prompt-sql-query-validation

Reference output for `example-input.sql` on PostgreSQL 16.4. Use it to sanity-check
what the model returns: a good run catches the two Criticals and most of the
High findings; missing F-01 or F-02 means the prompt context was ignored.

| ID | Severity | Category | Location | Issue |
| --- | --- | --- | --- | --- |
| F-01 | Critical | Dialect | `YEAR(o.created_at)` | `YEAR()` is not a PostgreSQL function — the query fails outright. |
| F-02 | Critical | Security | parameter binding | String interpolation into SQL is injection-prone; bind parameters. |
| F-03 | High | Correctness | `FROM orders o, users u` | Implicit comma join: any missing condition fans out rows silently. Write `JOIN ... ON`. |
| F-04 | High | Correctness | `o.status != 'cancelled'` | `status` is nullable; NULL rows are filtered silently. Decide if NULL means "active". |
| F-05 | High | Performance | `u.email LIKE '%@acme.com'` | Leading wildcard defeats btree indexes — Seq Scan on 120k users. Store the domain or add a `pg_trgm` index. |
| F-06 | Medium | Performance | `SELECT *` | Pulls every column including future PII; the report needs 4 columns. |
| F-07 | Medium | Performance | `ORDER BY`, no `LIMIT` | Sorts the full result set; paginate with `LIMIT` + keyset cursor. |
| F-08 | Medium | Performance | date filter | The F-01 fix must be a range predicate to stay sargable: `>= '2026-01-01' AND < '2027-01-01'`. |

## Corrected query (reference)

```sql
SELECT o.id, o.created_at, o.status, u.email
FROM orders o
JOIN users u ON u.id = o.user_id
WHERE u.email LIKE '%@acme.com'          -- see F-05 for index options
  AND o.created_at >= DATE '2026-01-01'
  AND o.created_at <  DATE '2027-01-01'
  AND (o.status IS NULL OR o.status <> 'cancelled')
ORDER BY o.created_at DESC
LIMIT 200;
```

## Verification

- `EXPLAIN (ANALYZE, BUFFERS)` before and after: the Seq Scan on `orders` should
  become an index-assisted read; p95 should land under the 500 ms SLA.
- Row-count equivalence on a staging copy: the corrected query may differ only
  by the documented NULL-status decision (F-04).
