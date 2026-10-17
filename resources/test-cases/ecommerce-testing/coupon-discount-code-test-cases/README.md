# Coupon & Discount Code Test Cases — Companion Files

Companion for [Coupon and Discount Code Test Cases](https://qapractices.com/test-cases/coupon-discount-code-test-cases/). The coupon test-data matrix, a reference discount-math implementation, and a runnable Playwright spec.

## Files

| File | Purpose |
| ---- | ------- |
| `coupons-test-data.csv` | Test data matrix for all 19 coupon codes used across TC001–TC033: type, value, min spend, category restriction, usage limits, validity range, expected result, mapped TCs. |
| `discount_calc.py` | Reference discount-math implementation (Decimal-based): percentage with half-up rounding, fixed capped at cart total, pre-tax min-spend check. Self-verifying asserts. |
| `playwright/tests/coupon.spec.js` | Self-contained spec (4 tests) covering percentage application, fixed-cap at total, min-spend rejection, and no-stacking — against an inline HTML coupon fixture. |

## Quick Start

```bash
python discount_calc.py          # runs the asserts for TC001/004/018/026/029
cd playwright && npm install && npx playwright test
```

## Requirements

- Python 3.10+ (stdlib only — `decimal`)
- Node.js 18+, `@playwright/test` 1.48+
