#!/usr/bin/env bash
# Non-GUI JMeter run + results checklist — the flags from the tutorial, runnable.
# Usage: JMETER_HOME=/path/to/apache-jmeter-5.6.3 ./run-load-test.sh test-plan.jmx
set -euo pipefail

PLAN="${1:-test-plan.jmx}"
JMETER="${JMETER_HOME:-.}/bin/jmeter"
STAMP="$(date +%Y%m%d-%H%M%S)"
RESULTS="results-${STAMP}.jtl"
REPORT="report-${STAMP}/"

if [ ! -f "$PLAN" ]; then
  echo "test plan not found: $PLAN" >&2
  exit 1
fi

echo "running $PLAN (non-GUI) → $RESULTS + $REPORT"
"$JMETER" -n -t "$PLAN" -l "$RESULTS" -e -o "$REPORT"

echo
echo "== post-run checklist =="
echo "[ ] error rate < 1%           → grep ',false,' $RESULTS | wc -l"
echo "[ ] p95 latency within SLO    → report-${STAMP}/index.html"
echo "[ ] throughput vs target rps  → dashboard graph"
echo "[ ] DLQ / retries clean       → server-side logs"
echo "[ ] report uploaded to CI     → artifact in $REPORT"
