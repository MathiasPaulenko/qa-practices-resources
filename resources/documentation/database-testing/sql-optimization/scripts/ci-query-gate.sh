#!/usr/bin/env bash
# ci-query-gate.sh <budget_ms> — fail if the benchmark query's actual time exceeds budget.
set -e
BUDGET=${1:-200}
DB=${DATABASE_URL:-postgresql://postgres:dev@localhost/postgres}
QUERY="SELECT * FROM orders WHERE status = 'shipped' AND customer_id = 4821 ORDER BY created_at DESC LIMIT 20"

ACTUAL=$(psql "$DB" -At -c "
  SELECT (plan->0->'Plan'->>'Actual Total Time')::numeric
  FROM (SELECT (EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) $QUERY)::jsonb AS plan) t;
")

echo "actual_total_time=${ACTUAL}ms budget=${BUDGET}ms"
awk -v a="$ACTUAL" -v b="$BUDGET" 'BEGIN { exit !(a <= b) }' || {
  echo "::error::Query regression — ${ACTUAL}ms exceeds ${BUDGET}ms budget"
  exit 1
}
echo "Query gate passed"
