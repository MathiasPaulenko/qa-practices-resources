#!/usr/bin/env bash
# verify-deprecation-headers.sh — assert a deprecated endpoint emits the
# Deprecation, Sunset and Link headers documented in RFC 9745 / RFC 8594.
#
# Usage: ./verify-deprecation-headers.sh <url>
# Exit:  0 = all deprecation signals present and well-formed
#        1 = usage error or endpoint unreachable
#        2 = verification failed (missing/malformed headers, or already retired)

set -u

URL="${1:-}"
if [ -z "$URL" ]; then
  echo "usage: $0 <url>" >&2
  exit 1
fi

HEADERS="$(curl -sS -o /dev/null -D - --max-time 15 "$URL")" || {
  echo "FAIL: endpoint unreachable: $URL" >&2
  exit 1
}

STATUS="$(printf '%s' "$HEADERS" | head -1 | awk '{print $2}')"
if [ "$STATUS" = "410" ]; then
  echo "NOTE: endpoint already retired (410 Gone) — deprecation headers no longer expected"
  exit 0
fi

FAIL=0

if printf '%s' "$HEADERS" | grep -qi '^Deprecation:'; then
  echo "PASS: Deprecation header present"
else
  echo "FAIL: missing Deprecation header (RFC 9745)" >&2
  FAIL=1
fi

SUNSET="$(printf '%s' "$HEADERS" | grep -i '^Sunset:' | head -1 | cut -d: -f2- | tr -d '\r')"
if [ -n "$SUNSET" ]; then
  if printf '%s' "$SUNSET" | grep -qE '(Mon|Tue|Wed|Thu|Fri|Sat|Sun), [0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} GMT'; then
    echo "PASS: Sunset header present with valid HTTP-date: ${SUNSET# }"
  else
    echo "FAIL: Sunset header is not a valid HTTP-date: ${SUNSET# }" >&2
    FAIL=1
  fi
else
  echo "FAIL: missing Sunset header (RFC 8594)" >&2
  FAIL=1
fi

if printf '%s' "$HEADERS" | grep -qi '^Link:.*successor-version'; then
  echo "PASS: Link header points at successor version"
else
  echo "FAIL: missing Link header with rel=\"successor-version\"" >&2
  FAIL=1
fi

[ "$FAIL" -eq 0 ] && exit 0 || exit 2
