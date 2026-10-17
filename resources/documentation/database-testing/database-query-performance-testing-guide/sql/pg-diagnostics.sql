-- PostgreSQL diagnostic pack for query performance testing
-- Requires: pg_stat_statements (shared_preload_libraries = 'pg_stat_statements')
-- Run: psql -h <staging-host> -U <user> -d <db> -f sql/pg-diagnostics.sql

-- 1) Top 10 queries by cumulative time — the real cost drivers
SELECT
  calls,
  ROUND(total_exec_time::numeric, 2) AS total_ms,
  ROUND(mean_exec_time::numeric, 2)  AS avg_ms,
  ROUND((100 * total_exec_time / NULLIF(SUM(total_exec_time) OVER (), 0))::numeric, 2) AS pct_of_load,
  LEFT(query, 120) AS query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- 2) Queries with the worst latency (candidates for index work)
SELECT
  calls,
  ROUND(mean_exec_time::numeric, 2) AS avg_ms,
  ROUND(max_exec_time::numeric, 2)  AS max_ms,
  LEFT(query, 120) AS query
FROM pg_stat_statements
WHERE calls >= 10
ORDER BY mean_exec_time DESC
LIMIT 10;

-- 3) Unused indexes — write overhead with zero reads
SELECT
  schemaname,
  relname AS table_name,
  indexrelname AS index_name,
  idx_scan,
  pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE idx_scan < 50
  AND schemaname = 'public'
ORDER BY pg_relation_size(indexrelid) DESC;

-- 4) Tables relying on sequential scans (missing index candidates)
SELECT
  relname AS table_name,
  seq_scan,
  seq_tup_read,
  idx_scan,
  pg_size_pretty(pg_relation_size(relid)) AS table_size,
  n_live_tup
FROM pg_stat_user_tables
WHERE seq_scan > 50
ORDER BY seq_tup_read DESC
LIMIT 15;

-- 5) Current lock waits — deadlocks and contention in the act
SELECT
  pid,
  now() - pg_stat_activity.query_start AS duration,
  wait_event_type,
  wait_event,
  state,
  LEFT(query, 100) AS query
FROM pg_stat_activity
WHERE wait_event IS NOT NULL
ORDER BY duration DESC;

-- 6) Buffer cache hit ratio — below 99% on OLTP means memory pressure
SELECT
  ROUND(100 * SUM(heap_blks_hit)::numeric / NULLIF(SUM(heap_blks_hit) + SUM(heap_blks_read), 0), 2) AS buffer_hit_pct
FROM pg_statio_user_tables;
