# Order Fulfillment & Shipping Testing

> Runnable companion for [Order Fulfillment & Shipping Testing Test Cases](https://qapractices.com/test-cases/order-fulfillment-shipping-testing/) — carrier-style webhook fixtures, a replay script, and a pytest suite for the tracking edge cases.

## Files

- `carrier-webhooks/` — eight tracking webhook payloads in carrier-event shape:
  - `01-label-created.json` → `04-delivered.json` — happy-path sequence.
  - `05-out-of-order-late-ofd.json` — late `out_for_delivery` arriving after `delivered`; the status must not regress.
  - `06-duplicate-in-transit.json` — exact replay of `02` (same `event_id`); must be idempotent.
  - `07-exception-lost.json`, `08-exception-damaged.json` — carrier exception events.
- `scripts/order_tracking_sim.py` — minimal state machine implementing the rules under test (idempotency, terminal-status preservation, exception flagging). Swap its internals for a call to your real handler.
- `scripts/replay_webhooks.py` — POSTs the fixtures to your webhook endpoint and prints the HTTP status per event.
- `scripts/test_webhook_edges.py` — pytest suite asserting the happy path, out-of-order preservation, duplicate idempotency, and exception handling.

## How to use

1. Run the edge-case suite against the reference state machine:

   ```bash
   cd scripts && pytest test_webhook_edges.py
   ```

2. Replay the fixtures against your own webhook receiver:

   ```bash
   python scripts/replay_webhooks.py --base-url http://localhost:8000/webhooks/tracking
   ```

3. Reproduce the out-of-order case manually: send `04-delivered.json` then `05-out-of-order-late-ofd.json` — the order status must remain `delivered`.

## Requirements

- Python 3.11+
- pytest 8.3+
- requests 2.32+ (only for `replay_webhooks.py`; the pytest suite is stdlib-only)

## Related

- [Order Fulfillment & Shipping Testing Test Cases](https://qapractices.com/test-cases/order-fulfillment-shipping-testing/) — the full suite this companion supports (TC-04, TC-08, and the edge-case table).
- [Inventory & Stock Management Test Cases](https://qapractices.com/test-cases/inventory-stock-management-testing/) — stock availability feeds the routing decisions.
