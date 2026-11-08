#!/usr/bin/env bash
# post-deploy-smoke.sh <base-url> — post-deploy smoke test.
#
# Asserts on response BODIES, not just status codes: a 200 serving a stale
# build is the classic false green. Credentials come from the environment —
# never hardcode a smoke account.
#
# Usage:
#   SMOKE_EMAIL=smoke@acme-corp.test SMOKE_PASSWORD=*** \
#     ./post-deploy-smoke.sh https://staging.acme-corp.test
#
# Requires: bash, curl, jq (1.6+)
# Exit codes: 0 all checks pass · 1 usage/unreachable · 2 a check failed

set -euo pipefail

BASE="${1:?Usage: $0 <base-url>  (set SMOKE_EMAIL and SMOKE_PASSWORD in the env)}"
: "${SMOKE_EMAIL:?set SMOKE_EMAIL for the dedicated smoke account}"
: "${SMOKE_PASSWORD:?set SMOKE_PASSWORD for the dedicated smoke account}"

echo "== Smoke test against $BASE =="

# 1. Health — verify the body marker, not just HTTP 200.
BODY=$(curl -sf --max-time 10 "$BASE/health") || { echo "FAIL: /health unreachable"; exit 1; }
echo "$BODY" | grep -q '"status":"ok"' || { echo "FAIL: /health body unexpected: $BODY"; exit 2; }
echo "health: PASS"

# 2. Auth — the login must return a usable token, not just 200.
TOKEN=$(curl -sf --max-time 10 -X POST "$BASE/api/login" \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"$SMOKE_EMAIL\",\"password\":\"$SMOKE_PASSWORD\"}" | jq -r '.token // empty')
[ -n "$TOKEN" ] || { echo "FAIL: login returned no token"; exit 2; }
echo "auth: PASS"

# 3. Protected endpoint — the token must actually work.
curl -sf --max-time 10 -H "Authorization: Bearer $TOKEN" "$BASE/api/orders?limit=1" >/dev/null \
  || { echo "FAIL: authenticated /api/orders rejected"; exit 2; }
echo "orders: PASS"

# 4. Version field — confirm the deployed build is the one expected, if provided.
if [ -n "${EXPECTED_VERSION:-}" ]; then
  DEPLOYED=$(curl -sf --max-time 10 "$BASE/version" | jq -r '.version // empty')
  [ "$DEPLOYED" = "$EXPECTED_VERSION" ] \
    || { echo "FAIL: deployed version '$DEPLOYED' != expected '$EXPECTED_VERSION' (stale build?)"; exit 2; }
  echo "version: PASS ($DEPLOYED)"
fi

echo "== smoke: all checks passed against $BASE =="
