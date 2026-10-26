#!/usr/bin/env bash
# observe-scaling.sh — apply the HPA, run the k6 stepped load and watch it react.
# Requires: kubectl 1.26+, k6 v2.3, a reachable cluster.
set -euo pipefail

kubectl apply -f hpa.yaml

BASE_URL="${BASE_URL:-https://staging.qapractices.com}" k6 run scalability-test.js &
K6_PID=$!

kubectl get hpa checkout-api --watch &
WATCH_PID=$!

wait "$K6_PID"
kill "$WATCH_PID" 2>/dev/null || true

kubectl top pods
