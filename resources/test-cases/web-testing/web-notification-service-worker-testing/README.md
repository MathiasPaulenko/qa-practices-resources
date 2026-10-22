# Web Notification & Service Worker Testing — Companion

Companion for [Web Notification & Service Worker Test Cases](https://qapractices.com/test-cases/web-notification-service-worker-testing/) ([versión en español](https://qapractices.com/es/test-cases/web-notification-service-worker-testing/)).

## What's inside

- `sw.js` — a real fixture service worker implementing the handlers the article tests: `install` precache, `activate` cache purge + `clients.claim()`, `fetch` offline fallback, `push` → `showNotification` inside `waitUntil`, `notificationclick` routing, `notificationclose` analytics.
- `sw_lifecycle.py` — stdlib-only model of the lifecycle states and push pipeline: registration scope, insecure-context refusal, install precaching, cache purge on activate, the waiting → `skipWaiting` update dance, stuck-update detection, push payload validation, 410 subscription expiry, and opt-out cleanup.
- `tests/test_sw_lifecycle.py` — pytest suite; each test is named after the `TC-xx` it covers so a failure points straight at the scenario.

## Run

```bash
pip install -r requirements.txt
pytest tests/
```

## Notes

- The real `sw.js` lifecycle can't run under pytest; use it as the page fixture for the Playwright spec in the article (`context.serviceWorkers()` + CDP `ServiceWorker.deliverPushMessage` on Chromium).
- On iOS, web push only works for PWAs installed to the Home Screen on iOS 16.4+ — see TC-18 in the article.
