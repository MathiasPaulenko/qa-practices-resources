# Webhook Integration Testing Plan — Companion

Runnable examples for the [Webhook Integration Testing Plan Template](https://qapractices.com/templates/webhook-integration-testing-plan-template/).

## Files

| File | What it does |
|---|---|
| `verify-signature.test.js` | Stripe-style HMAC signature verifier (`t=,v1=` header, timestamp tolerance, constant-time compare) with 6 `node:test` cases: valid, missing, tampered, wrong secret, expired, malformed. |
| `retry-simulator.js` | Retry + dead letter queue simulator. Prints the exponential backoff schedule and the outcome of six receiver behaviors — including the "400 never retried" and "retries exhausted → DLQ" paths. |
| `payload.sample.json` | The sample `payment.succeeded` payload used in the template's Section 2. |

## Run

```bash
node --test verify-signature.test.js   # 6 signature verification tests
node retry-simulator.js                # backoff schedule + 6 delivery scenarios
```

No dependencies — everything uses `node:crypto` and `node:test` (Node 18+).

## What it demonstrates

- **Signature verification beyond "does it parse"** — timestamp tolerance and constant-time comparison are the parts implementers skip and attackers use.
- **The retry matrix as executable truth** — which status codes retry, which fail fast, and when a delivery lands in the DLQ.
