#!/usr/bin/env bash
# OWASP ZAP 2.15 baseline scan against staging — writes zap-report.html.
# Env: BASE_URL
set -euo pipefail
: "${BASE_URL:?Set BASE_URL to a staging environment — never production}"

docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t "$BASE_URL" \
  -r zap-report.html
echo "Report written to zap-report.html — review high-severity alerts (XSS, SQLi, missing headers)"
