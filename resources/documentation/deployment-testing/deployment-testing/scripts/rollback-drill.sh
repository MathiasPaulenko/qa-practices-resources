#!/usr/bin/env bash
# rollback-drill.sh <base-url> [budget-seconds] — timed rollback rehearsal.
#
# A rollback that was never timed is a hypothesis. This script triggers your
# rollback command, measures how long the previous version takes to serve
# healthy again, and fails if it exceeds the budget — because that budget is
# your incident duration floor.
#
# Usage:
#   ROLLBACK_CMD='kubectl rollout undo deploy/api -n prod' \
#     ./rollback-drill.sh https://staging.acme-corp.test 120
#
# Requires: bash, curl, jq (1.6+), your rollback mechanism via ROLLBACK_CMD
# Exit codes: 0 within budget · 1 usage · 2 over budget or unhealthy after rollback

set -euo pipefail

BASE="${1:?Usage: $0 <base-url> [budget-seconds]  (set ROLLBACK_CMD in the env)}"
BUDGET="${2:-120}"
: "${ROLLBACK_CMD:?set ROLLBACK_CMD to your actual rollback command}"

echo "== Rollback drill against $BASE (budget: ${BUDGET}s) =="

echo "Executing: $ROLLBACK_CMD"
START=$(date +%s)
eval "$ROLLBACK_CMD"

# Poll health until the app serves again.
until curl -sf --max-time 5 "$BASE/health" | grep -q '"status":"ok"'; do
  sleep 2
  ELAPSED=$(( $(date +%s) - START ))
  if [ "$ELAPSED" -gt "$BUDGET" ]; then
    echo "FAIL: not healthy after ${BUDGET}s — rollback exceeded the budget" >&2
    exit 2
  fi
done

ELAPSED=$(( $(date +%s) - START ))
echo "Healthy again after ${ELAPSED}s"

# Re-verify the previous version actually works — same checks as the smoke test.
BODY=$(curl -sf --max-time 10 "$BASE/health")
echo "$BODY" | grep -q '"status":"ok"' || { echo "FAIL: post-rollback health body unexpected"; exit 2; }

if [ "$ELAPSED" -gt "$BUDGET" ]; then
  echo "FAIL: ${ELAPSED}s > ${BUDGET}s budget" >&2
  exit 2
fi

echo "== rollback drill PASS: service healthy in ${ELAPSED}s (budget ${BUDGET}s) =="
