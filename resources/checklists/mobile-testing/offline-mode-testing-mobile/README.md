# PWA Offline Testing Checklist — Companion

This companion provides runnable files for the [PWA Offline Testing Checklist](https://qapractices.com/checklists/offline-mode-testing-mobile) checklist.

## Files

| File | Purpose |
|------|---------|
| `src/workbox-register.js` | Workbox service worker registration with skip-waiting prompt |
| `src/indexeddb-read.js` | IndexedDB read example for offline data access |
| `src/network-transition-test.ts` | Playwright test for network transition (online to offline) |
| `src/background-sync-register.js` | Background Sync registration for queued requests |

## Quick Start

```bash
# Install Playwright
npm init -y && npm install @playwright/test

# Run the network transition test
npx playwright test src/network-transition-test.ts

# Serve the PWA locally and test Workbox registration
npx http-server . && open http://localhost:8080
```