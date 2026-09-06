#!/bin/bash
set -e

# Token Exchange Request (Authorization Code + PKCE)
# Usage: ./token-exchange.sh AUTH_CODE VERIFIER
# Requires: curl

AUTH_URL="https://auth.qa.local/oauth/token"
CLIENT_ID="web-client"
REDIRECT_URI="https://app.qa.local/callback"

if [ $# -lt 2 ]; then
  echo "Usage: $0 <AUTH_CODE> <CODE_VERIFIER>"
  exit 1
fi

AUTH_CODE="$1"
VERIFIER="$2"

curl -s -X POST "$AUTH_URL" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=${AUTH_CODE}" \
  -d "redirect_uri=${REDIRECT_URI}" \
  -d "client_id=${CLIENT_ID}" \
  -d "code_verifier=${VERIFIER}"
