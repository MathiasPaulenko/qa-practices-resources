# WebDriverIO vs Playwright — Companion

This companion provides runnable files for the [WebDriverIO 8 vs Playwright 1.45](https://qapractices.com/documentation/webdriverio-vs-playwright) decision guide.

## Files

| File | Purpose |
|------|---------|
| `tests/wdio.conf.ts` | WebDriverIO 8 config: Mocha + TypeScript, 4 parallel instances |
| `tests/appointments.wdio.spec.ts` | VitaCare appointment-booking test in WebDriverIO, including the `browser.mock` payment stub |
| `tests/playwright.config.ts` | Playwright 1.45 config: `fullyParallel`, chromium and webkit projects |
| `tests/appointments.pw.spec.ts` | The same appointment-booking test in Playwright, including the `page.route` payment stub |

## Quick Start

```bash
# WebDriverIO 8
npm install -D @wdio/cli @wdio/local-runner @wdio/mocha-framework @wdio/spec-reporter tsx
npx wdio run tests/wdio.conf.ts

# Playwright 1.45
npm install -D @playwright/test@1.45
npx playwright install chromium webkit
npx playwright test -c tests/playwright.config.ts
```

## Notes

- `browser.mock` requires WebDriver BiDi: local Chromium and Firefox, Selenium Grid 4+, or a cloud provider with BiDi enabled. On grids without BiDi, switch the spec to `page.route` in Playwright or a service-level stub.
- The specs point at `https://staging.vitacare.io`, the fictional staging app from the guide. Replace `baseURL` and the seeded `qa-patient@vitacare.io` account with your own environment and set `E2E_PASSWORD` before running.
