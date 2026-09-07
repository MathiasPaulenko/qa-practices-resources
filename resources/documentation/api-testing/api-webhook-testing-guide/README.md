# API Webhook Testing Guide — Companion Scripts

Companion resource for [API Webhook Guide: Delivery, Retries & Payload Integrity](https://qapractices.com/documentation/api-webhook-testing-guide).

## Contents

| File | Purpose |
|------|---------|
| `scripts/verify_signature.py` | HMAC-SHA256 signature verification over raw body (Python) |
| `scripts/stripe_consumer.js` | Express webhook consumer with signature check, queue and idempotency (Node.js) |
| `scripts/test_retry_behavior.py` | Simulate 200/400/500/410 responses and verify provider retry behavior |
| `scripts/docker-compose.yml` | Local ngrok + webhook.site setup for integration testing |
| `.github/workflows/webhook-tests.yml` | CI workflow running signature and retry tests |

## Quick Start

```bash
# Start the Stripe consumer
node scripts/stripe_consumer.js

# Expose it with ngrok
ngrok http 3000

# Run signature verification tests
python scripts/verify_signature.py

# Run retry behavior tests
python scripts/test_retry_behavior.py
```

## Requirements

- Python 3.10+
- Node.js 18+
- ngrok (for local integration testing)

## Related Resource

- [API Webhook Guide](https://qapractices.com/documentation/api-webhook-testing-guide)
- [Spanish version](https://qapractices.com/es/documentation/api-webhook-testing-guide)
