#!/usr/bin/env bash
# benchmark.sh <runs> — N timed executions of the benchmark query.
# Uses \timing so each run reports real elapsed ms, warm cache included.
set -e
RUNS=${1:-50}
DB=${DATABASE_URL:-postgresql://postgres:dev@localhost/postgres}
QUERY="SELECT * FROM orders WHERE status = 'shipped' AND customer_id = 4821 ORDER BY created_at DESC LIMIT 20;"

total=0; min=999999; max=0
for i in $(seq 1 "$RUNS"); do
  ms=$(psql "$DB" -At -c "SELECT count(*) FROM (SELECT 1) x WHERE (SELECT extract(epoch from now()) IS NOT NULL); SELECT clock_timestamp()" -c "\timing on" -c "$QUERY" 2>/dev/null | grep -oP 'Time: \K[0-9.]+' | tail -1)
  [ -z "$ms" ] && continue
  total=$(echo "$total + $ms" | bc)
  min=$(echo "if ($ms < $min) $ms else $min" | bc)
  max=$(echo "if ($ms > $max) $ms else $max" | bc)
done
avg=$(echo "scale=2; $total / $RUNS" | bc)
echo "runs=$RUNS min=${min}ms avg=${avg}ms max=${max}ms"
