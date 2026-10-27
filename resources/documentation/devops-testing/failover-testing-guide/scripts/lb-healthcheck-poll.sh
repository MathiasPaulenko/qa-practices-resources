#!/usr/bin/env bash
# lb-healthcheck-poll.sh — poll the load balancer while a backend is killed.
# Every non-200 line is a user-facing error during the failover transition.
# Usage: BASE_URL=https://staging.qapractices.com ./lb-healthcheck-poll.sh
set -u

BASE_URL="${BASE_URL:-https://staging.qapractices.com/health}"
INTERVAL="${INTERVAL:-2}"
ERRORS=0
TOTAL=0

echo "Polling ${BASE_URL} every ${INTERVAL}s — press Ctrl+C to stop."
trap 'echo; echo "Total: ${TOTAL} requests, ${ERRORS} non-200"; exit 0' INT

while true; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "${BASE_URL}")
  TOTAL=$((TOTAL + 1))
  if [ "${code}" != "200" ]; then
    ERRORS=$((ERRORS + 1))
    echo "$(date +%H:%M:%S) -> ${code}  <-- user-facing error"
  else
    echo "$(date +%H:%M:%S) -> ${code}"
  fi
  sleep "${INTERVAL}"
done
