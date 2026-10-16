# Payment Security Testing — Runnable Companion

Companion repository for the QAPractices guide
[Payment Security Testing Guide: PCI DSS & Fraud](https://qapractices.com/documentation/payment-security-testing/)
([versión en español](https://qapractices.com/es/documentation/payment-security-testing/)).

Self-contained: the mock payment API is a stdlib `http.server` fixture, so the
attack tests run without any external service or real gateway credentials.

## Layout

```text
mock_payment_server.py        stdlib fixture API: server-side amount validation,
                              Idempotency-Key dedup, HMAC webhook verification
tests/test_payment_security.py  pytest 8.2 attack regression suite (7 tests)
requirements.txt              requests 2.31.0, pytest 8.2.0
```

## Run the suite

```bash
python -m venv venv
source venv/bin/activate    # venv\Scripts\activate on Windows
pip install -r requirements.txt
pytest tests/test_payment_security.py -v
```

`mock_payment_server.py` spins up inside the pytest fixture on an ephemeral
port. To poke it manually, run `python mock_payment_server.py` and it listens on
`http://127.0.0.1:8765`.

## What the tests prove

| Test | Attack simulated | Pass criteria |
|---|---|---|
| `test_amount_tampering_is_rejected` | Client sends `amount: 0.01` for a $99.99 order | 400 `amount mismatch`, no charge created |
| `test_currency_tampering_is_rejected` | Currency swapped without recomputation | 400, no charge created |
| `test_idempotent_replay_creates_single_charge` | Same request replayed with the same `Idempotency-Key` | Same charge id returned, exactly one charge recorded |
| `test_forged_webhook_signature_is_rejected` | Fake `payment.succeeded` event with garbage signature | 401, event not recorded |
| `test_replayed_webhook_outside_tolerance_is_rejected` | Correctly signed webhook with a 1-hour-old timestamp | 401 |
| `test_valid_signed_webhook_is_accepted` | Properly signed, fresh webhook | 200, event recorded |
| `test_webhook_signed_with_wrong_secret_is_rejected` | Valid format signed with an attacker secret | 401 |

The signature scheme mirrors Stripe's `t=timestamp,v1=hmac_sha256` header —
swap `WEBHOOK_SECRET` for your endpoint secret and the same `sign_webhook`
helper exercises your real staging endpoint.
