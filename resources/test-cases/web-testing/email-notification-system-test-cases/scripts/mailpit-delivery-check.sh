#!/usr/bin/env bash
# Poll a Mailpit inbox until a message for the given recipient arrives,
# then assert on subject and List-Unsubscribe header.
# Usage: ./mailpit-delivery-check.sh ana.martinez@taskflow.io "task assigned"
# Requires: Mailpit running (docker run -p 8025:8025 axllent/mailpit) and jq.
set -euo pipefail

MAILPIT_API="${MAILPIT_API:-http://localhost:8025/api/v1}"
RECIPIENT="${1:?recipient email required}"
SUBJECT_MATCH="${2:-task assigned}"
TIMEOUT="${TIMEOUT:-60}"

deadline=$((SECONDS + TIMEOUT))
while (( SECONDS < deadline )); do
  msg_id=$(curl -s "${MAILPIT_API}/search?query=to:${RECIPIENT}" | jq -r '.messages[0].ID // empty')
  if [[ -n "$msg_id" ]]; then
    msg=$(curl -s "${MAILPIT_API}/message/${msg_id}")
    subject=$(echo "$msg" | jq -r '.Subject')
    list_unsub=$(echo "$msg" | jq -r '.Message["List-Unsubscribe"] // empty')
    echo "Subject: $subject"
    echo "List-Unsubscribe: ${list_unsub:-MISSING}"
    [[ "$subject" == *"$SUBJECT_MATCH"* ]] || { echo "FAIL: subject does not contain '$SUBJECT_MATCH'"; exit 1; }
    [[ -n "$list_unsub" ]] || { echo "FAIL: List-Unsubscribe header missing"; exit 1; }
    echo "PASS: delivery verified"
    exit 0
  fi
  sleep 2
done

echo "FAIL: no email for ${RECIPIENT} within ${TIMEOUT}s"
exit 1
