#!/usr/bin/env bash
# Repeat a spec N times to prove (or disprove) flakiness.
# Usage: ./repeat-until-failure.sh login.spec.ts [runs]
set -u

SPEC="${1:?usage: $0 <spec-file> [runs]}"
RUNS="${2:-20}"

echo "repeating $SPEC up to $RUNS times — first failure means it's flaky"
for i in $(seq 1 "$RUNS"); do
  if ! npx playwright test "$SPEC" --reporter=line > /tmp/flaky-run.log 2>&1; then
    echo "FLAKY at run $i — output:"
    tail -15 /tmp/flaky-run.log
    exit 1
  fi
done
echo "$RUNS/$RUNS clean — test is deterministic under this loop"
