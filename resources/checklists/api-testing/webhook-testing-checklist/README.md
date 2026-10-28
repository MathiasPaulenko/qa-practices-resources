# Webhook Testing Checklist — Companion

Companion resource for [Webhook Testing Checklist: Delivery, Payload & Signatures](https://qapractices.com/checklists/webhook-testing-checklist).

## Contents

- `webhook-verify.mjs` — Standard-Webhooks-style signature verifier (`{id}.{timestamp}.{payload}` with HMAC-SHA256, constant-time compare, 5-minute tolerance) plus the matching `sign()` helper
- `receiver.mjs` — minimal HTTP receiver that verifies the signature, deduplicates by `webhook-id`, returns 2xx only after durable receipt
- `send-test-webhook.mjs` — CLI client that signs real payloads and can replay the same event ID to exercise deduplication
- `tests/verify.test.mjs` — node:test suite covering valid signatures, tampered payloads, wrong event IDs, stale timestamps, missing headers, unsigned requests and duplicate delivery
- `package.json` — scripts, zero runtime dependencies

## Requirements

- Node.js 20+ (uses `node:test` and global `fetch`, no installs needed)

## Usage

```bash
node --test                 # run the suite, no server needed for verifier tests
node receiver.mjs           # start the receiver on http://localhost:3000/webhooks
node send-test-webhook.mjs --resend   # send a signed event, then replay the same event ID
```

The signature scheme follows the [Standard Webhooks](https://github.com/standard-webhooks/standard-webhooks) convention used in the checklist: the secret stays in `WEBHOOK_SECRET`, the timestamp stays inside the tolerance window, and duplicates are answered with a plain 200 so the sender stops retrying.
