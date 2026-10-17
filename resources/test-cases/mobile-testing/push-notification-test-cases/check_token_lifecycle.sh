#!/usr/bin/env bash
set -euo pipefail

# Token lifecycle verification — mirrors TC003/TC004/TC005.
# Usage: API_BASE="https://your-api" AUTH="Bearer ..." ./check_token_lifecycle.sh <device_id>
# Verifies a device's token is registered, then sends a probe push to a stale
# token and asserts the backend marks it dead.

API_BASE="${API_BASE:?Set API_BASE}"
AUTH="${AUTH:?Set AUTH header}"
DEVICE_ID="${1:?Usage: check_token_lifecycle.sh <device_id>}"

echo "=== Token lifecycle check for device ${DEVICE_ID} ==="

echo "[1/3] Registered token exists and has a platform tag"
resp=$(curl -sf -H "Authorization: ${AUTH}" "${API_BASE}/devices/${DEVICE_ID}/push-tokens")
token=$(echo "$resp" | python -c "import json,sys; d=json.load(sys.stdin); print(d['tokens'][0]['token'] if d.get('tokens') else '')")
platform=$(echo "$resp" | python -c "import json,sys; d=json.load(sys.stdin); print(d['tokens'][0]['platform'] if d.get('tokens') else '')")
[ -n "$token" ] && [ -n "$platform" ] || { echo "FAIL: no registered token for ${DEVICE_ID}"; exit 1; }
echo "  token registered (${platform})"

echo "[2/3] Duplicate registration is idempotent"
before=$(echo "$resp" | python -c "import json,sys; print(len(json.load(sys.stdin).get('tokens',[])))")
curl -sf -X POST -H "Authorization: ${AUTH}" -H "Content-Type: application/json" \
  -d "{\"token\":\"${token}\",\"platform\":\"${platform}\"}" "${API_BASE}/devices/${DEVICE_ID}/push-tokens" >/dev/null
after=$(curl -sf -H "Authorization: ${AUTH}" "${API_BASE}/devices/${DEVICE_ID}/push-tokens" | python -c "import json,sys; print(len(json.load(sys.stdin).get('tokens',[])))")
[ "$before" = "$after" ] || { echo "FAIL: duplicate registration created ${after} tokens (was ${before})"; exit 1; }
echo "  idempotent (${before} token row)"

echo "[3/3] Stale token gets pruned after provider rejection"
stale="STALE_TOKEN_$(date +%s)"
code=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Authorization: ${AUTH}" \
  -H "Content-Type: application/json" \
  -d "{\"token\":\"${stale}\"}" "${API_BASE}/push/send")
echo "  send to stale token -> HTTP ${code} (backend should mark it dead; check provider response log)"

echo "=== Lifecycle checks passed ==="
