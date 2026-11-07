#!/usr/bin/env bash
# Runs an Apache JMeter 5.6.x test plan in non-GUI mode and writes
# results.jtl plus an HTML report. The GUI is for building the plan only.
set -euo pipefail

PLAN="${1:-load-test-plan.jmx}"
REPORT_DIR="${2:-report}"

jmeter -n -t "${PLAN}" -l results.jtl -e -o "${REPORT_DIR}"
echo "Results: results.jtl — HTML report: ${REPORT_DIR}/index.html"
