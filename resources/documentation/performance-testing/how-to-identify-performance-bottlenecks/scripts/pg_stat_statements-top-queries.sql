-- Find the queries that hurt most.
-- Requires: PostgreSQL 15+, pg_stat_statements enabled
--   (CREATE EXTENSION IF NOT EXISTS pg_stat_statements;)
-- Run: psql -d yourdb -f pg_stat_statements-top-queries.sql

-- Top queries by total time — the ones that cost the most overall,
-- not just the slowest average.
SELECT
  calls,
  mean_exec_time,
  total_exec_time,
  rows,
  shared_blks_hit,
  shared_blks_read,
  query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Queries never hitting an index (seq scans on hot paths).
-- After spotting one, EXPLAIN ANALYZE it before adding an index.
SELECT
  calls,
  mean_exec_time,
  query
FROM pg_stat_statements
WHERE query NOT LIKE '%INDEX%'
ORDER BY calls DESC
LIMIT 20;
