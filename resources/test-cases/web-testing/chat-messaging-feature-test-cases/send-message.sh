#!/usr/bin/env bash
# REST API examples — set API and TOKEN first:
#   export API=https://api.staging.example.com/v1 TOKEN=xxx
set -euo pipefail

API="${API:-https://api.staging.example.com/v1}"
CONV="${CONV_ID:-CONV-5001}"

# TC001 — send a text message
curl -sS -X POST "$API/conversations/$CONV/messages" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"text":"Hello, can you review the PR?"}' | jq '.id, .status'

# TC012 — fetch history with pagination (first 50, then older page)
curl -sS "$API/conversations/$CONV/messages?limit=50" \
  -H "Authorization: Bearer $TOKEN" | jq '.messages | length'
curl -sS "$API/conversations/$CONV/messages?limit=50&before=<oldest_message_id>" \
  -H "Authorization: Bearer $TOKEN" | jq '.messages | length'

# TC003 — mark messages as read (fires the read receipt)
curl -sS -X POST "$API/conversations/$CONV/read" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"upToMessageId":"<message_id>"}'
