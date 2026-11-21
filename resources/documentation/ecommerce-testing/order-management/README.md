# Order Management Testing — State Machine & Idempotency Suite

Runnable pytest 8.x suite for the [Order Management Testing guide](https://qapractices.com/documentation/order-management/).

## Files

- `test_order_transitions.py` — parametrized valid/invalid transition tests + payment idempotency invariant.
- `sample-order.json` — sample order payload (totals, line items, idempotency key).

## Run

```bash
pip install pytest==8.3.4
pytest test_order_transitions.py -v
```

All tests are self-contained — `FakeGateway` and `Order` stubs simulate the payment capture so the idempotency invariant runs without external services.
