#!/bin/bash
# Contract check: verify GET returns 200 for a valid order ID
TOKEN="${API_TOKEN:-test-token}"
BASE="${API_BASE:-https://staging.lumapay.com/api/v1}"

status=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  "${BASE}/orders/123")

echo "Status: $status"
if [ "$status" = "200" ]; then
  echo "PASS: GET /orders/123 returned 200"
  exit 0
else
  echo "FAIL: expected 200, got $status"
  exit 1
fi
