#!/usr/bin/env bash
# Headless runner — JMeter 5.6.3+. Builds a dashboard in ./report.
set -euo pipefail

PLAN="$(dirname "$0")/login-token-pattern.jmx"
OUT="$(dirname "$0")"

jmeter -n \
  -t "$PLAN" \
  -l "$OUT/results.jtl" \
  -e -o "$OUT/report/"

echo "Done. Open $OUT/report/index.html for the dashboard."
