# Playwright API Cheat Sheet — Runnable Companion

Copy-paste `@playwright/test` 1.x snippets companion to the [Playwright API Cheat Sheet](https://qapractices.com/documentation/playwright-api-cheat-sheet/) on QAPractices.

## Contents

`typescript/` holds one file per cheat-sheet section:

| File | Covers |
|---|---|
| `browser-context.ts` | Launching browsers and isolated `BrowserContext` |
| `navigation.ts` | `goto`, history, `waitForURL`, `waitForLoadState` |
| `locators.ts` | `page.locator()` and `getBy*` locators, chaining, filtering |
| `actions.ts` | Click, fill, press, select, check, drag, file upload |
| `assertions.ts` | Retrying `expect` assertions (web-first) |
| `auto-waiting.ts` | `locator.waitFor()` states and `setDefaultTimeout` |
| `network.ts` | `page.route`, `waitForResponse`, `page.request` |
| `dialogs.ts` | `page.on('dialog')` handler (register before triggering) |
| `screenshots.ts` | Page, full-page and element screenshots |
| `multiple-pages.ts` | Capturing new tabs via `context.waitForEvent('page')` |
| `fixtures-hooks.ts` | Built-in `page` fixture, `beforeEach`/`afterEach` |
| `playwright.config.ts` | Timeouts, retries, baseURL, artifacts on failure |

## Usage

These are reference snippets, not a runnable suite — most operate on a `page`/`context`/`browser` provided by your test or REPL session. To try them in a real project:

```bash
npm init playwright@latest
npx playwright test
```

See the cheat sheet for the notes on when each call applies and the common pitfalls (auto-waiting, dialog ordering, `networkidle`).
