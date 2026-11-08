#!/usr/bin/env bash
# provoke-429.sh — burst an endpoint until it 429s and report the boundary.
#
# Verifies the limit actually enforces: sends N rapid requests, counts the
# status codes, and reports which request number first got rejected. The
# boundary matters more than the wall — request N passing and N+1 getting
# 429 is the off-by-one check most rate limiters fail.
#
# Usage:
#   ./provoke-429.sh https://api.acme-corp.test/search [burst-size]
#
# Exit codes:
#   0 — a 429 boundary was found (limit enforces)
#   1 — usage error or endpoint unreachable
#   2 — no 429 seen inside the burst (limit missing or higher than burst size)

set -euo pipefail

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo "Usage: $0 <url> [burst-size]" >&2
  echo "Example: $0 https://api.acme-corp.test/search 30" >&2
  exit 1
fi

URL="$1"
BURST="${2:-30}"

echo "== Provoking 429 on $URL (burst of $BURST) =="

FIRST_429=""
declare -a CODES=()

for i in $(seq 1 "$BURST"); do
  CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$URL") || {
    echo "FAIL: request $i could not reach $URL" >&2
    exit 1
  }
  CODES+=("$CODE")
  if [ -z "$FIRST_429" ] && [ "$CODE" = "429" ]; then
    FIRST_429=$i
  fi
done

echo "Status codes: ${CODES[*]}"
echo

# Any 5xx in the mix is a separate bug — the limiter should reject, not break.
for c in "${CODES[@]}"; do
  if [[ "$c" =~ ^5 ]]; then
    echo "FAIL: got HTTP $c — the limiter broke instead of rejecting." >&2
    exit 2
  fi
done

if [ -z "$FIRST_429" ]; then
  echo "FAIL: no 429 in $BURST requests." >&2
  echo "Either no limit is enforced or it sits above the burst — raise the burst size and rerun." >&2
  exit 2
fi

if [ "$FIRST_429" -eq 1 ]; then
  echo "PASS: 429 from request 1 — a previous window is already exhausted, or the limit is 0."
else
  echo "PASS: boundary at request $FIRST_429 — requests 1..$((FIRST_429 - 1)) passed, request $FIRST_429 got 429."
fi
echo "Check Retry-After before retrying: ./verify-rate-limit-headers.sh $URL"
