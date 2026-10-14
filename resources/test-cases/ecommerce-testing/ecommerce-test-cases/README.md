# E-commerce Test Cases — Runnable Playwright Spec

Companion repository for the QAPractices resource
[E-commerce Test Cases: Practical QA Test Cases for Teams](https://qapractices.com/test-cases/ecommerce-test-cases/)
([versión en español](https://qapractices.com/es/test-cases/ecommerce-test-cases/)).

Self-contained: every fixture renders inline with `page.setContent()`, so the
spec needs no store backend. It demonstrates the assertions behind the cart
cases (TC-001 to TC-005), the stock display case (TC-032) and the coupon math
case (TC-034) from the suite.

## Layout

```text
playwright/   @playwright/test 1.48.2
```

## Run

```bash
cd playwright
npm install
npx playwright test
```

The config uses `channel: 'chrome'` — it runs your installed Chrome, so no
browser download is needed. For CI, remove the channel option and run
`npx playwright install chromium` to use the bundled browser.

## What the spec covers

- **Add two products** — badge count, cart lines and `$44.49` subtotal.
- **Quantity update** — `1 → 3` recalculates the line total and `$89.97` subtotal.
- **Remove one item** — the other item survives, subtotal drops to `$29.99`.
- **Zero stock** — the add button is disabled and reads `Out of stock`.
- **Coupon math** — `SUMMER20` turns a `$44.49` subtotal into `$35.59`;
  an invalid code reports `Invalid coupon`.

All five tests pass on Chrome stable with Playwright 1.48.
