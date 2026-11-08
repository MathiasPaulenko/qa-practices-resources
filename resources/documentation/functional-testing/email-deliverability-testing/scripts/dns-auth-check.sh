#!/usr/bin/env bash
# dns-auth-check.sh — verify SPF, DKIM and DMARC for a sending domain.
# Usage: dns-auth-check.sh example.com [dkim-selector]
set -u

DOMAIN="${1:?usage: dns-auth-check.sh example.com [dkim-selector]}"
SELECTOR="${2:-s1}"
FAILURES=0

echo "== SPF ($DOMAIN) =="
if dig TXT "$DOMAIN" +short | grep -q 'v=spf1'; then
  dig TXT "$DOMAIN" +short | grep 'v=spf1'
else
  echo "MISSING: no v=spf1 record"
  FAILURES=$((FAILURES + 1))
fi

echo "== DKIM ($SELECTOR._domainkey.$DOMAIN) =="
if dig TXT "$SELECTOR._domainkey.$DOMAIN" +short | grep -qE 'k=|p='; then
  dig TXT "$SELECTOR._domainkey.$DOMAIN" +short
else
  echo "MISSING: no DKIM public key for selector $SELECTOR"
  FAILURES=$((FAILURES + 1))
fi

echo "== DMARC (_dmarc.$DOMAIN) =="
if dig TXT "_dmarc.$DOMAIN" +short | grep -q 'v=DMARC1'; then
  dig TXT "_dmarc.$DOMAIN" +short
else
  echo "MISSING: no DMARC record"
  FAILURES=$((FAILURES + 1))
fi

if [ "$FAILURES" -gt 0 ]; then
  echo "RESULT: $FAILURES record(s) missing — do not send until fixed"
  exit 1
fi
echo "RESULT: all authentication records present"
