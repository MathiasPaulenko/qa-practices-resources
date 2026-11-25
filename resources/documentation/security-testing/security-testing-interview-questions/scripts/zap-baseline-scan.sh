#!/usr/bin/env bash
# OWASP ZAP 2.14.0 baseline scan — passive scan against a staging target.
# Usage: ./zap-baseline-scan.sh https://staging.your-app.example
# Requires Docker. Writes zap-report.html to the working directory.
set -euo pipefail

TARGET="${1:?Usage: $0 <target-url>}"

docker run -t -v "$(pwd):/zap/wrk/:rw" ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
  -t "$TARGET" \
  -r zap-report.html
