#!/usr/bin/env bash
# OWASP ZAP baseline scan — passive scan of a running app via Docker.
# Usage: ./zap-baseline.sh https://staging.example.com
# Requires: Docker. The `stable` tag tracks the ZAP 2.15 line.

set -euo pipefail

TARGET_URL="${1:?Usage: $0 <target-url>}"

docker run -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
  -t "$TARGET_URL" \
  -r zap-baseline.html
