#!/bin/bash
# Rate limit test for API gateway

BASE="https://api.staging.local"
ENDPOINT="$BASE/api/v1/data"
API_KEY="test-key"

echo "=== Sending 110 sequential requests ==="
for i in {1..110}; do
  CODE=$(curl -s -o /dev/null -w "%{http_code}" -H "api-key: $API_KEY" "$ENDPOINT")
  echo "Request $i: $CODE"
  if [ "$CODE" = "429" ]; then
    echo "Rate limit hit at request $i"
    echo "=== Rate limit headers ==="
    curl -s -I -H "api-key: $API_KEY" "$ENDPOINT" | grep -i "X-RateLimit\|Retry-After"
    break
  fi
done