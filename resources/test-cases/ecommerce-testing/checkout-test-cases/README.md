# Checkout Test Cases — Companion Files

Companion for [Checkout Test Cases: Payment & Shipping](https://qapractices.com/test-cases/checkout-test-cases/). Runnable Playwright spec plus the Stripe test-card matrix used throughout the resource.

## Files

| File | Purpose |
| ---- | ------- |
| `stripe-test-cards.csv` | Stripe test card matrix: card number → expected behavior → decline code → scenario id. Import into your data-driven suite. |
| `playwright/tests/checkout.spec.js` | Self-contained Playwright spec (4 tests) exercising decline messaging, double-submit idempotency, and the free-shipping boundary — against an inline HTML checkout fixture, no backend needed. |

## Quick Start

```bash
cd playwright
npm install
npx playwright install chromium
npm test
```

## Requirements

- Node.js 18+
- `@playwright/test` 1.48+

The spec renders a self-contained checkout page inline (`page.setContent`), so it runs without a store or gateway. The decline map mirrors Stripe's documented test cards — swap the fixture for your staging checkout to run the same cases end-to-end.
