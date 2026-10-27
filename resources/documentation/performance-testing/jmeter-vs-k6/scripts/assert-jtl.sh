#!/usr/bin/env bash
# assert-jtl.sh — fail the build if the JMeter error rate exceeds the threshold.
# Usage: ./scripts/assert-jtl.sh results.jtl 0.005
# Expects a CSV-format .jtl with a header row (JMeter 5.6.3 defaults).

set -euo pipefail

JTL_FILE="${1:?usage: assert-jtl.sh <results.jtl> <max-error-rate>}"
MAX_RATE="${2:?usage: assert-jtl.sh <results.jtl> <max-error-rate>}"

if [ ! -f "$JTL_FILE" ]; then
  echo "assert-jtl: file not found: $JTL_FILE" >&2
  exit 2
fi

total=$(awk -F',' 'NR>1 {n++} END {print n+0}' "$JTL_FILE")
failed=$(awk -F',' 'NR>1 && $8=="false" {n++} END {print n+0}' "$JTL_FILE")

if [ "$total" -eq 0 ]; then
  echo "assert-jtl: no samples in $JTL_FILE" >&2
  exit 2
fi

rate=$(awk -v f="$failed" -v t="$total" 'BEGIN {printf "%.6f", f/t}')
echo "assert-jtl: $failed/$total failed (rate=$rate, max=$MAX_RATE)"

awk -v r="$rate" -v m="$MAX_RATE" 'BEGIN {exit (r > m) ? 1 : 0}'
