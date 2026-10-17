#!/usr/bin/env bash
set -euo pipefail

# Post-deployment smoke tests — run immediately after a production deploy.
# Usage: BASE_URL="https://your-host" API_KEY="..." ./smoke-test.sh
# Exit code 1 + non-zero FAIL = evaluate rollback.

BASE_URL="${BASE_URL:?Set BASE_URL to your environment}"
API_KEY="${API_KEY:?Set API_KEY}"
PASS=0; FAIL=0

smoke() {
  local label="$1" method="$2" endpoint="$3" expected="$4"
  local status
  status=$(curl -s -o /dev/null -w "%{http_code}" -X "$method" \
    "${BASE_URL}${endpoint}" -H "Authorization: Bearer ${API_KEY}")
  if [ "$status" = "$expected" ]; then
    echo "[PASS] $label (HTTP $status)"; PASS=$((PASS+1))
  else
    echo "[FAIL] $label — expected $expected, got $status"; FAIL=$((FAIL+1))
  fi
}

echo "=== Post-Deployment Smoke Tests ==="
echo "Target: ${BASE_URL}"
echo ""

# Adapt these endpoints to your critical paths.
smoke "Health check"         GET  "/health"      200
smoke "Readiness probe"      GET  "/ready"       200
smoke "Login endpoint"       POST "/auth/login"  200
smoke "Core listing"         GET  "/products"    200
smoke "Current user"         GET  "/users/me"    200
smoke "Unauthorized guarded" GET  "/admin"       401

echo ""
echo "=== Results: ${PASS} passed, ${FAIL} failed ==="
if [ "$FAIL" -gt 0 ]; then
  echo "ALERT: ${FAIL} smoke checks failed — evaluate rollback"
  exit 1
fi
echo "All smoke checks passed — release is healthy"
