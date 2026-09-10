#!/bin/bash
# Verify steady-state before and after chaos experiments

METRICS_URL="http://monitoring.staging.local/metrics"
MAX_ERROR_RATE=1
MAX_P99_LATENCY=500

echo "=== Steady-state verification ==="

# Check error rate
ERROR_RATE=$(curl -s "$METRICS_URL" | grep "http_requests_total" | awk '{print $2}')
echo "Error rate: $ERROR_RATE% (max: $MAX_ERROR_RATE%)"

# Check p99 latency
P99_LATENCY=$(curl -s "$METRICS_URL" | grep "http_request_duration_p99" | awk '{print $2}')
echo "p99 latency: ${P99_LATENCY}ms (max: ${MAX_P99_LATENCY}ms)"

# Check pod count
POD_COUNT=$(kubectl get pods -n staging -l app=payments-service --field-selector=status.phase=Running --no-headers | wc -l)
echo "Healthy pods: $POD_COUNT"

# Validate
if (( $(echo "$ERROR_RATE > $MAX_ERROR_RATE" | bc -l) )); then
  echo "FAIL: Error rate exceeds threshold"
  exit 1
fi

if (( $(echo "$P99_LATENCY > $MAX_P99_LATENCY" | bc -l) )); then
  echo "FAIL: p99 latency exceeds threshold"
  exit 1
fi

if [ "$POD_COUNT" -lt 1 ]; then
  echo "FAIL: No healthy pods"
  exit 1
fi

echo "PASS: Steady-state verified"
exit 0