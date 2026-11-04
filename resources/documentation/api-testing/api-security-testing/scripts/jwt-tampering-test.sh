#!/usr/bin/env bash
# JWT tampering probe — token with altered payload / invalid signature must be rejected.
# Also craft alg:none and RS256->HS256 confusion variants outside this script.
# Expected: 401 Unauthorized. Env: BASE_URL, TAMPERED_TOKEN
set -euo pipefail
: "${BASE_URL:?Set BASE_URL to a staging API}"
: "${TAMPERED_TOKEN:?Set TAMPERED_TOKEN to a token with modified payload}"

code=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $TAMPERED_TOKEN" \
  "$BASE_URL/v1/profile")
echo "HTTP $code"
[ "$code" = "401" ] || { echo "FAIL: tampered token accepted ($code)"; exit 1; }
echo "PASS"
