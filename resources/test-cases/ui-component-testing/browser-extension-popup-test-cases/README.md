# Browser Extension Popup Test Cases — Companion

Runnable materials for the [Browser Extension Popup Test Cases](https://qapractices.com/test-cases/browser-extension-popup-test-cases/) resource on QAPractices.

## Contents

| File | What it is |
|---|---|
| `extension/manifest.json` | Minimal Manifest V3 manifest: `storage` permission, `activeTab` as optional, service-worker background, action popup. |
| `extension/popup.html` | TabSaver-style popup: note input, Save button, saved-pages list, compact-view toggle and dark-mode styles. |
| `extension/popup.js` | Popup logic: loads state from `chrome.storage.local` on open, requests `activeTab` on click, saves entries, shows a retryable error when the worker doesn't answer. |
| `extension/background.js` | MV3 service worker with a `chrome.runtime.onMessage` handler using `sendResponse`. |
| `popup-persistence.spec.ts` | Playwright 1.48 spec: launches a persistent context with the extension loaded, opens `chrome-extension://{id}/popup.html`, saves a page and verifies the list rehydrates from storage after reopen. |
| `package.json` | `@playwright/test` dependency and the `test` script. |

## Quick start

```bash
# Install the Playwright runner (Node 18+)
npm install
npx playwright install chromium

# Run the spec (headed — persistent contexts need a real window)
npm test
```

To try the popup manually, load `extension/` as an unpacked extension at `chrome://extensions` with Developer mode on.

## Notes

- Extensions only load inside a **persistent context** (`chromium.launchPersistentContext`); a normal `browser.newContext()` won't pick them up. For CI use `--headless=new` — the legacy headless mode doesn't run extensions.
- The popup is destroyed on blur: every open re-runs `loadState()` and rehydrates the UI from `chrome.storage.local`. That cold-start behavior is what TC-006 verifies.
- The background service worker can sleep after ~30 idle seconds; the first `sendMessage` afterwards exercises the wake-up path covered by TC-012.
