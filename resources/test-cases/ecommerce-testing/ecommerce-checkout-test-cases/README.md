# E-commerce Checkout Test Cases — Cart-to-Order Engine

Companion for the [E-commerce Checkout Test Cases: Cart to Order](https://qapractices.com/test-cases/ecommerce-checkout-test-cases/) resource on QAPractices.

## What's inside

- **`checkout_flow.py`** — a pure-stdlib cart→order state machine: cart lines, coupons with minimum-subtotal and one-per-order rules, free-shipping threshold, guest/registered accounts, cart merge on login, idempotent `place_order` keyed like Stripe's idempotency keys, orders, order history and guest lookup.
- **`tests/test_checkout_flow.py`** — 17 pytest cases mapped 1:1 to `TC-001`..`TC-016` in the resource, plus a bonus assertion on the `card_declined` → HTTP 402 + preserved-cart path.
- **`requirements.txt`** — just pytest.

## Run it

```bash
pip install -r requirements.txt
pytest tests/ -q
```

Expected: `17 passed`.

## Mapping

Each test is named after the test case it verifies — `test_tc011` is the double-submit idempotency check, `test_tc016` the guest lookup leakage check. The simulated gateway uses the real [Stripe test card numbers](https://docs.stripe.com/testing): `4242 4242 4242 4242` succeeds, `4000 0000 0000 0002` declines.
