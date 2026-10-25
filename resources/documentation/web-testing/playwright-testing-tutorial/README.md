# Playwright Testing Tutorial — Runnable Companion

Runnable starter project for the [Playwright Testing Tutorial: Setup, Selectors, Assertions](https://qapractices.com/documentation/playwright-testing-tutorial/) on QAPractices.

## Contents

| File | Matches tutorial step |
|---|---|
| `package.json` | Step 1 — `@playwright/test` dev dependency |
| `playwright.config.ts` | Step 2/10 — three browser projects, retries, trace on first retry |
| `tests/first-test.spec.ts` | Step 3 — title assertion on playwright.dev |
| `tests/locators.spec.ts` | Step 4 — role, text and test-id locators |
| `tests/network-mock.spec.ts` | Step 7 — `page.route` interception with a stubbed JSON response |
| `.github/workflows/playwright.yml` | Step 10 — CI job with browser install, sharding and report artifact |

## Usage

```bash
npm install
npx playwright install --with-deps
npx playwright test
```

The specs target `https://playwright.dev` so they run without a local server. To point them at your own app, change the URLs and locators — the structure stays the same.
