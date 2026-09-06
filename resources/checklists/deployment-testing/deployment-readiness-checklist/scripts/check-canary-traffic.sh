#!/bin/bash
set -e

# Canary Traffic Shift Verification
# Verifies that canary traffic is within the expected range (1-10%).
# Usage: ./check-canary-traffic.sh
# Requires: jq 1.6+, curl

TRAFFIC_MANAGER="https://lb.qa.local"
SERVICE="checkout"

WEIGHT=$(curl -s "${TRAFFIC_MANAGER}/services/${SERVICE}/weight" | jq '.canary')
if [ "$WEIGHT" -gt 0 ] && [ "$WEIGHT" -le 10 ]; then
  echo "Canary traffic is at ${WEIGHT}%"
else
  echo "Canary weight is not in expected range: ${WEIGHT}"
  exit 1
fi
