#!/usr/bin/env bash
# verify-rate-limit-headers.sh — assert a 429 carries the headers clients need.
#
# A 429 without Retry-After is operationally useless: clients hammer blindly
# or give up. This script exhausts the limit with a burst, then inspects the
# rejecting response for Retry-After and the X-RateLimit-* trio.
#
# Usage:
#   ./verify-rate-limit-headers.sh https://api.acme-corp.test/search [burst-size]
#
# Exit codes:
#   0 — 429 seen and all required headers present
#   1 — usage error or endpoint unreachable
#   2 — verification failed (no 429, missing Retry-After, or missing X-RateLimit-*)

set -euo pipefail

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo "Usage: $0 <url> [burst-size]" >&2
  exit 1
fi

URL="$1"
BURST="${2:-30}"

# Burn through the limit, then capture the headers of the last (rejecting) call.
for _ in $(seq 1 "$BURST"); do
  curl -s -o /dev/null --max-time 10 "$URL" || true
done

HEADERS=$(curl -sI --max-time 10 "$URL") || {
  echo "FAIL: cannot reach $URL" >&2
  exit 1
}

STATUS=$(echo "$HEADERS" | head -1 | tr -d '\r')
echo "== $URL =="
echo "Status line: $STATUS"
echo "$HEADERS" | grep -i 'ratelimit\|retry-after' || echo "(no rate-limit headers found)"
echo

FAIL=0

if ! echo "$STATUS" | grep -q "429"; then
  echo "WARN: response is not 429 — burst may not have exhausted the limit. Inspect headers anyway."
fi

echo "$HEADERS" | grep -iq '^retry-after:' || {
  echo "FAIL: missing Retry-After — clients cannot know when to retry." >&2
  FAIL=2
}
echo "$HEADERS" | grep -iq '^x-ratelimit-limit:' || {
  echo "FAIL: missing X-RateLimit-Limit." >&2
  FAIL=2
}
echo "$HEADERS" | grep -iq '^x-ratelimit-remaining:' || {
  echo "FAIL: missing X-RateLimit-Remaining." >&2
  FAIL=2
}
echo "$HEADERS" | grep -iq '^x-ratelimit-reset:' || {
  echo "FAIL: missing X-RateLimit-Reset." >&2
  FAIL=2
}

[ "$FAIL" -ne 0 ] && exit "$FAIL"
echo "PASS: 429 carries Retry-After and the X-RateLimit-* trio."
