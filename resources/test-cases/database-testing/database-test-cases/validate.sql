-- Post-migration validation queries for database-test-cases (PostgreSQL 12+)
-- Run after schema or data migrations to confirm integrity survived.

-- 1. Constraints on orders: expect PK, FK, CHECK, DEFAULT to be listed
SELECT
  tc.constraint_name,
  tc.constraint_type,
  kcu.column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
  ON tc.constraint_name = kcu.constraint_name
WHERE tc.table_name = 'orders'
ORDER BY tc.constraint_type;

-- 2. Orphan check: orders referencing missing users (expect 0 rows)
SELECT o.id, o.user_id
FROM orders o
LEFT JOIN users u ON u.id = o.user_id
WHERE u.id IS NULL;

-- 3. NULL check on required columns (expect 0 on all)
SELECT
  COUNT(*) FILTER (WHERE email IS NULL) AS null_emails,
  COUNT(*) FILTER (WHERE name IS NULL) AS null_names,
  COUNT(*) FILTER (WHERE status IS NULL) AS null_status
FROM users u
FULL JOIN orders o ON false;

-- 4. Negative totals violating the domain rule (expect 0 rows)
SELECT id, total FROM orders WHERE total < 0;
