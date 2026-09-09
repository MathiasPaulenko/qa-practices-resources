# PWA Testing Guide Companion

Companion resource for the [PWA Testing Guide](https://qapractices.com/documentation/pwa-testing-guide). Contains a runnable Workbox setup, Playwright PWA tests, a valid web app manifest, and a CI workflow.

## Files

| File | Purpose |
|------|---------|
| `workbox-config.js` | Workbox 7.4.1 configuration for generating a service worker |
| `sw.js` | Custom service worker with NetworkFirst, CacheFirst, and StaleWhileRevalidate strategies |
| `manifest.json` | Valid web app manifest with 192x192 and 512x512 icons |
| `playwright.config.ts` | Playwright config pinned to Chromium with `serviceWorkers: 'allow'` |
| `tests/offline.spec.ts` | Offline smoke test — verifies app shell loads when network is cut |
| `tests/installability.spec.ts` | Installability test — verifies `beforeinstallprompt` fires |
| `.github/workflows/pwa-tests.yml` | CI workflow that builds, generates SW, starts HTTPS tunnel, and runs Playwright |

## Quick Start

```bash
npm install --save-dev workbox-cli@7.4.1 @playwright/test
npx workbox generateSW workbox-config.js
npx playwright test tests/
```

## CI

The included GitHub Actions workflow runs on every push and PR:

1. Installs dependencies
2. Builds the project
3. Generates the service worker with Workbox
4. Starts an HTTPS tunnel with `localtunnel`
5. Runs Playwright PWA tests

## Requirements

- Node.js 22+
- Workbox CLI 7.4.1
- Playwright 1.50+
- A build output in `dist/`
