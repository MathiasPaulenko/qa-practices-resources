-- Missing-index example from the guide.
-- Run twice: once before CREATE INDEX (expect Seq Scan), once after (Index Scan / Index Only Scan).

-- Optional seed (creates the table if it does not exist and inserts sample rows)
CREATE TABLE IF NOT EXISTS orders (
  order_id   bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id    bigint NOT NULL,
  total      numeric(10,2) NOT NULL,
  status     text NOT NULL DEFAULT 'paid',
  created_at timestamptz NOT NULL DEFAULT now()
);

-- EXPLAIN ANALYZE — look for "Seq Scan on orders" and actual time
EXPLAIN ANALYZE
SELECT order_id, total, created_at
FROM orders
WHERE user_id = 12345
ORDER BY created_at DESC
LIMIT 20;

-- The fix — composite index matching the WHERE + ORDER BY
-- Uncomment, run, then re-run the EXPLAIN ANALYZE above.
-- CREATE INDEX CONCURRENTLY idx_orders_user_id_created_at
--   ON orders(user_id, created_at DESC);
