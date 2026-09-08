# Shopping Cart & Wishlist Testing — Companion Tests and Fixtures

> Companion resource for [Shopping Cart & Wishlist Testing](https://qapractices.com/test-cases/shopping-cart-wishlist-testing-test-cases) on QAPractices.com.

Playwright specs, API test helpers and test data fixtures for shopping cart and wishlist testing with Playwright 1.48 and pytest 8.3.

## Requirements

- Node.js 20+
- Playwright 1.48
- Python 3.12+
- pytest 8.3
- requests 2.32

## Setup

```bash
# Install Playwright
npm install @playwright/test@1.48
npx playwright install

# Install Python dependencies
pip install pytest==8.3 requests==2.32

# Run Playwright cart tests
npx playwright test tests/cart.spec.ts

# Run API price calculation tests
pytest tests/test_price_calc.py

# Run cross-device sync tests
npx playwright test tests/cross-device.spec.ts --project=mobile
```

## Files

| File | Purpose |
| ------ | --------- |
| `tests/cart.spec.ts` | Playwright spec for add, remove, quantity update and price verification |
| `tests/wishlist.spec.ts` | Playwright spec for wishlist add, move to cart and stock validation |
| `tests/cross-device.spec.ts` | Playwright spec for cross-device cart synchronization |
| `tests/test_price_calc.py` | pytest test for subtotal, discount, tax and grand total calculation |
| `tests/test_inventory.py` | pytest test for inventory limits and overselling prevention |
| `fixtures/products.json` | Test data: SKUs, prices, stock levels and promo codes |
| `fixtures/users.json` | Test users: authenticated, guest and cross-device sessions |
| `.github/workflows/cart-tests.yml` | CI workflow for cart and wishlist regression tests |

## Test Data

The `fixtures/` directory contains reusable test data:

- `products.json` — SKUs with prices, stock levels and per-customer limits
- `users.json` — authenticated users, guest sessions and cross-device scenarios

## License

MIT — free to use, modify, and distribute. Never test against production payment systems; always use test cards and synthetic users.
