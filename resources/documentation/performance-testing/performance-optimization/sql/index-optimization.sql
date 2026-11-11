-- Index patterns from the Performance Optimization Guide (PostgreSQL).

-- Exact match lookups
CREATE INDEX idx_email ON users(email);

-- Range queries: composite, most-filtered column first
CREATE INDEX idx_created ON orders(created_at, status);

-- Full-text search
CREATE INDEX idx_search ON articles USING gin(search_vector);

-- JSON queries
CREATE INDEX idx_meta ON logs USING gin(metadata);

-- Geospatial
CREATE INDEX idx_loc ON stores USING gist(location);

-- Always measure before and after
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT o.id, o.total, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.created_at > '2026-01-01'
ORDER BY o.total DESC
LIMIT 100;

-- Maintenance: find unused indexes
SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;

-- Maintenance: index bloat (needs pgstattuple extension)
-- SELECT * FROM pgstattuple('idx_email');
