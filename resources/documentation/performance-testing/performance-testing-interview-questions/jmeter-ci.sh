#!/usr/bin/env bash
# jmeter-ci.sh — non-GUI JMeter run for CI pipelines (Q15 of the guide).
# Requires Apache JMeter 5.6.x on PATH.
set -euo pipefail

TEST_PLAN="${1:-load-test.jmx}"
RESULTS="results-$(date +%Y%m%d-%H%M%S).jtl"
REPORT_DIR="report-$(date +%Y%m%d-%H%M%S)"

# -n non-GUI, -t test plan, -l results log, -e/-o HTML report output
jmeter -n -t "${TEST_PLAN}" -l "${RESULTS}" -e -o "${REPORT_DIR}"

echo "Results: ${RESULTS}"
echo "HTML report: ${REPORT_DIR}/index.html"
