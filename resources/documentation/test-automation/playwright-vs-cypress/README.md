# Playwright vs Cypress — Companion

This companion provides runnable files for the [Playwright vs Cypress: E2E Decision Matrix](https://qapractices.com/documentation/playwright-vs-cypress) guide.

## Files

| File | Purpose |
|------|---------|
| `tests/playwright-3ds.spec.ts` | Playwright 1.61.1 test for Adyen 3DS challenge flow |
| `tests/cypress-3ds.cy.js` | Cypress 15.18.1 test for Adyen 3DS challenge flow |
| `tests/playwright.config.ts` | Playwright config with projects for chromium, firefox, webkit and mobile |
| `.github/workflows/playwright-e2e.yml` | GitHub Actions workflow with 4-shard parallel execution |
| `.github/workflows/cypress-e2e.yml` | GitHub Actions workflow for Cypress (single machine) |

## Quick Start

```bash
# Install dependencies
npm install -D @playwright/test cypress

# Run Playwright 3DS test
npx playwright test tests/playwright-3ds.spec.ts

# Run Cypress 3DS test
npx cypress run --spec tests/cypress-3ds.cy.js

# Run Playwright with sharding (CI)
npx playwright test --shard=1/4 --workers=4
```

## CI Integration

The included GitHub Actions workflows run Playwright (4 shards) and Cypress (single machine) on every push and pull request.