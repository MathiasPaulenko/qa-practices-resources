#!/usr/bin/env bash
# post-deploy-verify.sh — verify a hotfix actually landed in production.
#
# A green health check on the old artifact is the most common false positive
# in hotfix verification. This script checks three things: the endpoint
# responds, the version field matches what you deployed, and latency is
# inside baseline. Requires curl and jq.
#
# Usage:
#   ./post-deploy-verify.sh https://api.acme-corp.test/health 1.2.4-hotfix
#
# Exit codes:
#   0 — all checks pass
#   1 — usage error or endpoint unreachable
#   2 — verification failed (wrong version or slow response) → start the
#       rollback clock, don't wait for it to "settle"

set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <health-url> <expected-version>" >&2
  echo "Example: $0 https://api.acme-corp.test/health 1.2.4-hotfix" >&2
  exit 1
fi

URL="$1"
EXPECTED="$2"
LATENCY_LIMIT_MS=2000

echo "== Post-deploy verification =="
echo "URL:              $URL"
echo "Expected version: $EXPECTED"
echo

START=$(date +%s%N)
BODY=$(curl -fsS --max-time 10 "$URL") || {
  echo "FAIL: endpoint unreachable or non-2xx." >&2
  echo "Start the rollback clock — do not wait for it to settle." >&2
  exit 1
}
END=$(date +%s%N)
LATENCY_MS=$(( (END - START) / 1000000 ))

VERSION=$(echo "$BODY" | jq -r '.version // empty')
STATUS=$(echo "$BODY" | jq -r '.status // "unknown"')

echo "HTTP status:      OK"
echo "Reported status:  $STATUS"
echo "Reported version: $VERSION"
echo "Latency:          ${LATENCY_MS}ms (limit ${LATENCY_LIMIT_MS}ms)"
echo

if [ -z "$VERSION" ]; then
  echo "FAIL: no 'version' field in the health response." >&2
  echo "Status 200 alone proves nothing — the endpoint must tell you what is running." >&2
  exit 2
fi

if [ "$VERSION" != "$EXPECTED" ]; then
  echo "FAIL: version mismatch — running '$VERSION', expected '$EXPECTED'." >&2
  echo "The deploy did not land. Check the pipeline, then roll back." >&2
  exit 2
fi

if [ "$LATENCY_MS" -gt "$LATENCY_LIMIT_MS" ]; then
  echo "FAIL: latency ${LATENCY_MS}ms above the ${LATENCY_LIMIT_MS}ms limit." >&2
  echo "The fix landed but degraded the service — check error rates before deciding." >&2
  exit 2
fi

echo "PASS: version $VERSION verified in ${LATENCY_MS}ms."
echo "Keep watching dashboards for 30 minutes — gradual degradation won't show here."
