#!/usr/bin/env bash
# seed-send.sh — send a tracked test message to every address in a seed list
# through your real SMTP relay, then print the token to poll with
# tests/seed_inbox_check.py.
# Usage: seed-send.sh seeds.txt from@yourdomain.com
# Env:   SMTP_HOST, SMTP_PORT (default 587), SMTP_USER, SMTP_PASS
set -u

SEED_FILE="${1:?usage: seed-send.sh seeds.txt from@yourdomain.com}"
FROM="${2:?usage: seed-send.sh seeds.txt from@yourdomain.com}"
SMTP_PORT="${SMTP_PORT:-587}"

: "${SMTP_HOST:?set SMTP_HOST}" "${SMTP_USER:?set SMTP_USER}" "${SMTP_PASS:?set SMTP_PASS}"

TOKEN="deliv-$(date +%s)"
DOMAIN="${FROM#*@}"
echo "Token: $TOKEN"

while IFS= read -r seed; do
  [ -z "$seed" ] && continue
  swaks --to "$seed" \
        --from "$FROM" \
        --server "$SMTP_HOST:$SMTP_PORT" \
        --tls --auth LOGIN \
        --auth-user "$SMTP_USER" --auth-password "$SMTP_PASS" \
        --h-Subject "Deliverability test $TOKEN" \
        --h-List-Unsubscribe "<mailto:unsubscribe@$DOMAIN>" \
        --body "Seed test $TOKEN — check Authentication-Results and folder placement" \
        >/dev/null 2>&1 \
    && echo "sent -> $seed" \
    || echo "FAILED -> $seed"
done < "$SEED_FILE"

echo "Done. Poll each seed mailbox with token: $TOKEN"
