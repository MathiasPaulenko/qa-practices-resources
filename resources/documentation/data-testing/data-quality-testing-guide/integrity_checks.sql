-- Data quality checks from the Data Quality Guide
-- https://qapractices.com/documentation/data-quality-testing-guide/
-- Run against PostgreSQL 15+; adapt table/column names to your schema.

-- 1. Referential integrity: orphan orders without a customer.
-- Expected: zero rows. If any row returns, stop the pipeline.
SELECT *
FROM orders
WHERE customer_id NOT IN (SELECT id FROM customers);

-- 2. Uniqueness: duplicate customer IDs.
-- Expected: zero rows.
SELECT customer_id, COUNT(*)
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- 3. Daily profile on transactions — the baseline for anomaly detection.
-- Track these numbers over time; a profile without a baseline is just a statistic.
SELECT
  AVG(amount) AS avg_amount,
  STDDEV(amount) AS stddev_amount,
  MIN(amount) AS min_amount,
  MAX(amount) AS max_amount,
  COUNT(*) AS row_count
FROM transactions
WHERE transaction_date = CURRENT_DATE;

-- 4. Load reconciliation: source vs target row counts.
-- Expected: identical cnt in both rows.
SELECT 'source' AS system, COUNT(*) AS cnt FROM source.orders
UNION ALL
SELECT 'target', COUNT(*) FROM warehouse.fact_orders;

-- 5. Value-level reconciliation between source and target.
-- Expected: zero rows; tolerance of 0.01 for float drift.
SELECT
  s.order_id,
  s.total AS source_total,
  t.total AS target_total
FROM source.orders s
JOIN warehouse.fact_orders t ON s.order_id = t.order_id
WHERE ABS(s.total - t.total) > 0.01;
