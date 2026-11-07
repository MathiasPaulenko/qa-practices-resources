# Webhook Test Cases — Runnable Companion

Deterministic, stdlib-only Python model of a webhook delivery: Stripe-style HMAC signing (`t=<ts>,v1=<hmac_sha256(secret, "{t}.{body}")>`), a consumer that verifies, deduplicates, orders and processes events, and a provider that retries with exponential backoff into a dead-letter queue. The pytest suite maps TC-01..TC-12 from the [webhook test cases](https://qapractices.com/test-cases/webhook-test-cases/) on qapractices.com — no network, no sleeping, fully reproducible.

## Requirements

- Python 3.10+
- `pytest` (see `requirements.txt`, pinned 8.3.x)

## Run

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Files

| Path | Purpose |
|---|---|
| `webhook_pipeline.py` | `sign()`/`verify_signature()` (constant-time compare + timestamp tolerance), `Consumer` (signature→parse→dedup→ordering→apply), `Provider` (backoff schedule + dead-letter), `validate_endpoint()` for TLS checks |
| `tests/test_webhook_cases.py` | One test per TC: valid/forged/stale signatures, replay window, idempotency, out-of-order, backoff schedule, malformed payloads, unknown types, secret rotation, TLS validation, dead-lettering |
| `tests/conftest.py` | Path setup so tests import the simulator |
| `fixtures/signed-event.json` | Sample payload + how to regenerate its signature header |

## What to adapt for a real provider

- Header shape: swap `SCHEME`/`sign()` for the provider's format (`X-Hub-Signature-256: sha256=...` for GitHub, `Stripe-Signature` for Stripe).
- Tolerance: 300 s is the common default; Stripe uses 5 min, configure yours.
- Retry schedule: `Provider(schedule=[...])` takes the real backoff; add jitter via `jitter=`.
- Dedup TTL: `Consumer.seen` is in-memory here — production needs a store (Redis/DB) with a TTL longer than the provider's retry window.
