-- Index strategies from the guide. Run CONCURRENTLY on a live table;
-- drop CONCURRENTLY for a disposable test database.
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_customer_status_created
ON orders (customer_id, status, created_at DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_covering
ON orders (customer_id, status, created_at DESC)
INCLUDE (total, tracking_number);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_shipped_recent
ON orders (created_at DESC)
WHERE status = 'shipped';
