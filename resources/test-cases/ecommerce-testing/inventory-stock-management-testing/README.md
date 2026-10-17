# Inventory & Stock Management Test Cases — Companion Files

Companion for [Inventory & Stock Management Test Cases](https://qapractices.com/test-cases/inventory-stock-management-testing/). A runnable concurrency test for overselling, reorder/phantom-stock SQL checks, and a Behave-ready Gherkin suite.

## Files

| File | Purpose |
| ---- | ------- |
| `reservation_test.py` | pytest + `requests` concurrency test. Fires 10 simultaneous reservations at one remaining unit and asserts exactly one succeeds — the invariant that catches overselling. |
| `reorder_alert.sql` | Two diagnostic queries: products past their reorder threshold with no alert, and phantom stock (system > 0, warehouse = 0). |
| `inventory.feature` | Gherkin scenarios for overselling prevention, reservation TTL expiry, reorder alerts and FEFO allocation — ready for Behave or Cucumber. |

## Quick Start

```bash
pip install pytest requests
API_BASE_URL=https://staging.yourstore.test/api pytest reservation_test.py -v
```

Seed `SKU123` with `stock=1` on the target API before running — the test
asserts exactly one reservation succeeds, so a richer seed makes it pass for
the wrong reason.

## Requirements

- Python 3.10+
- `pytest` 8.x, `requests` 2.32+
- A staging inventory API exposing `POST /api/reserve` (or adapt `reserve_stock` to your endpoints)
- Behave 1.3+ or Cucumber, if you want to drive `inventory.feature`
