#!/usr/bin/env bash
# green_gate.sh — exits 0 only when every health endpoint on green answers 200.
# Usage: GREEN_URL=https://green.internal ./green_gate.sh
set -euo pipefail

GREEN_URL="${GREEN_URL:?set GREEN_URL to the green environment base URL}"
MAX_ATTEMPTS="${MAX_ATTEMPTS:-30}"
SLEEP_SECONDS="${SLEEP_SECONDS:-10}"
ENDPOINTS=("/health" "/health/db" "/health/cache")

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  ok=0
  for ep in "${ENDPOINTS[@]}"; do
    code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "${GREEN_URL}${ep}")
    if [ "$code" = "200" ]; then
      ok=$((ok + 1))
    else
      echo "attempt ${attempt}: ${ep} -> HTTP ${code}"
    fi
  done
  if [ "$ok" -eq "${#ENDPOINTS[@]}" ]; then
    echo "green ready after ${attempt} attempt(s)"
    exit 0
  fi
  sleep "$SLEEP_SECONDS"
done

echo "green never became ready after ${MAX_ATTEMPTS} attempts" >&2
exit 1
