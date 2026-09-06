# PWA Testing Guide — Companion Scripts

Companion scripts for the [PWA Testing Guide](https://qapractices.com/documentation/progressive-web-app-pwa-testing-guide).

## Files

| File | Purpose |
| --- | --- |
| `scripts/manifest.json` | Valid web app manifest with `id`, icons, and standalone display. |
| `scripts/workbox-config.js` | Workbox 7 routing with CacheFirst, NetworkFirst, and StaleWhileRevalidate strategies. |
| `scripts/playwright-offline-test.js` | Playwright 1.48 test: verifies the app shell loads offline after first visit. |
| `scripts/playwright-install-prompt-test.js` | Playwright 1.48 test: verifies `beforeinstallprompt` is deferrable. |
| `scripts/lighthouse-ci-config.json` | Lighthouse 12 CI config with PWA score threshold of 90. |

## Usage

```bash
# Install dependencies
npm install workbox-routing@7 workbox-strategies@7
npm install -D @playwright/test@1.48 lighthouse@12

# Run Playwright PWA tests
npx playwright test scripts/playwright-offline-test.js
npx playwright test scripts/playwright-install-prompt-test.js

# Run Lighthouse CI
npx lighthouse-ci --config=scripts/lighthouse-ci-config.json https://pwa.qa.local
```

## Requirements

- Node.js 20+
- Playwright 1.48+
- Lighthouse 12+
- Workbox 7+
