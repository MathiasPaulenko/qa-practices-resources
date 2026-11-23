#!/usr/bin/env bash
# check-version-negotiation.sh — probe an API's version negotiation rules:
# valid version, missing version (default), invalid version, and conflicting
# URL-vs-header indicators.
#
# Usage: ./check-version-negotiation.sh <base-url> <valid-version> <invalid-version>
# Example: ./check-version-negotiation.sh https://api.acme.dev v1 v99
# Exit:  0 = documented behavior observed
#        1 = usage error
#        2 = one or more probes returned an undocumented status

set -u

BASE="${1:-}"
GOOD="${2:-}"
BAD="${3:-}"
if [ -z "$BASE" ] || [ -z "$GOOD" ] || [ -z "$BAD" ]; then
  echo "usage: $0 <base-url> <valid-version> <invalid-version>" >&2
  exit 1
fi

FAIL=0

probe() {
  local name="$1" url="$2" accept="$3" expect="$4"
  local code
  code="$(curl -sS -o /dev/null -w '%{http_code}' --max-time 15 \
    ${accept:+-H "Accept: $accept"} "$url")"
  if [ "$code" = "500" ]; then
    echo "FAIL: $name -> HTTP 500 (invalid input must never 500)" >&2
    FAIL=1
  elif [ "$expect" = "2xx" ] && [ "${code:0:1}" = "2" ]; then
    echo "PASS: $name -> HTTP $code"
  elif [ "$expect" = "4xx" ] && [ "${code:0:1}" = "4" ]; then
    echo "PASS: $name -> HTTP $code"
  else
    echo "FAIL: $name -> HTTP $code (expected $expect)" >&2
    FAIL=1
  fi
}

probe "valid version path"        "$BASE/$GOOD/users" ""                                  "2xx"
probe "missing version"           "$BASE/users"       ""                                  "2xx-or-4xx-per-default"
probe "non-existent version"      "$BASE/$BAD/users"  ""                                  "4xx"
probe "non-numeric version header" "$BASE/users"     "application/vnd.api+json;version=abc" "4xx"
probe "conflicting indicators"    "$BASE/$GOOD/users" "application/vnd.api+json;version=$BAD" "documented-precedence"

# "missing version" and "conflicting indicators" are reported but not enforced:
# the correct status depends on the documented default / precedence rule.
[ "$FAIL" -eq 0 ] && exit 0 || exit 2
