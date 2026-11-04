#!/usr/bin/env bash
# BOLA/IDOR probe — replay a request with a different resource ID.
# Expected: 403 Forbidden or 404 Not Found — never another user's data.
# Env: BASE_URL (staging only), USER_A_TOKEN
set -euo pipefail
: "${BASE_URL:?Set BASE_URL to a staging API, e.g. https://staging.example.com}"
: "${USER_A_TOKEN:?Set USER_A_TOKEN to a dedicated test-account token}"

echo "[*] Own resource — expect 200"
curl -s -o /dev/null -w "HTTP %{http_code}\n" \
  -H "Authorization: Bearer $USER_A_TOKEN" \
  "$BASE_URL/v1/orders/1234"

echo "[*] Other user's resource — expect 403 or 404"
code=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $USER_A_TOKEN" \
  "$BASE_URL/v1/orders/1235")
echo "HTTP $code"
[ "$code" = "403" ] || [ "$code" = "404" ] || { echo "FAIL: returned $code, possible BOLA"; exit 1; }
echo "PASS"
