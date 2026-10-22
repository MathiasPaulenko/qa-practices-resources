# Subscription Billing Test Cases — Companion

Executable pytest suite for the [Subscription and Billing Test Cases](https://qapractices.com/test-cases/subscription-billing-test-cases/) resource on QAPractices.

`conftest.py` ships pure-Python reference implementations of the billing logic that goes wrong most often: integer-cent proration, dunning schedules, webhook idempotency (ledger dedupe), trial expiry and cancel-state rules. The suite exercises the boundary cases — last day of cycle, day-zero windows, replayed events, cardless trial expiry.

## Run

```bash
pip install -r requirements.txt
pytest tests/ -v          # 16 tests
```

## Covers

- Proration: mid-cycle upgrade, day 0/day 30 boundaries, half-up rounding, annual→monthly credit
- Dunning: retry schedule offsets
- Webhooks: duplicate delivery no-op, out-of-order events, charge vs credit separation
- Lifecycle: trial active/expired/with-card, immediate vs period-end cancel
