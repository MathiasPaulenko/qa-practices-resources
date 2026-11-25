# Test Automation Troubleshooting — Companion

Runnable Playwright examples for the [Test Automation Troubleshooting Guide](https://qapractices.com/documentation/test-automation-troubleshooting/).

## Requirements

- Node.js 26.13.1
- `@playwright/test` 1.65.1 (locked in `package-lock.json`)
- Chromium installed by Playwright

## Run

```bash
npm ci
npx playwright install chromium
npm test
```

The tests use isolated Playwright fixtures and an inline page, so they do not need an application server, database, or credentials. `pipeline-status.spec.ts` demonstrates waiting for an observable status instead of sleeping; `selector-contract.spec.ts` uses a role-based locator.

The GitHub Actions workflow uses full commit SHAs for its actions. Replace the inline page with your app's staging route only after configuring `baseURL`, test data, and service readiness in your own project.
