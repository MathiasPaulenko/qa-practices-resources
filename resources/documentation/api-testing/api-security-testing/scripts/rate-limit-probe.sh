#!/usr/bin/env bash
# Rate limiting probe — 100 rapid requests; expect 429 + Retry-After past the threshold.
# Env: BASE_URL, USER_A_TOKEN
set -euo pipefail
: "${BASE_URL:?Set BASE_URL to a staging API}"
: "${USER_A_TOKEN:?Set USER_A_TOKEN to a dedicated test-account token}"

hits=0
for i in $(seq 1 100); do
  code=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer $USER_A_TOKEN" \
    "$BASE_URL/v1/orders")
  [ "$code" = "429" ] && hits=$((hits+1))
done
echo "429 responses: $hits/100"
[ "$hits" -gt 0 ] || { echo "FAIL: no rate limiting detected"; exit 1; }
echo "PASS — verify a Retry-After header is also returned"
