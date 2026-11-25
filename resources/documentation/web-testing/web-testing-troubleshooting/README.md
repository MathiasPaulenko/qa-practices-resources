# Web Testing Troubleshooting — Companion

Runnable snippets referenced in the [Web Testing Troubleshooting Guide](https://qapractices.com/documentation/web-testing-troubleshooting/) on QAPractices.

## Files

| File | Problem it solves |
|---|---|
| `explicit-waits.js` | Fixed sleeps → condition-based waits for flaky CI tests (Problem 1) |
| `stable-selectors.js` | `data-testid` selectors instead of browser-dependent pseudo-classes (Problem 2) |
| `playwright-ci.config.ts` | Timeout, retry, viewport and launch-arg overrides for slower CI runners (Problem 3) |
| `visual-mask.js` | Element masking to keep ads, timestamps and avatars out of visual diffs (Problem 4) |
| `shard-ci.sh` | Playwright `--shard` split across 4 GitHub Actions runners (Problem 5) |

## Usage

- Requires `@playwright/test` 1.65 or later for the JS/TS snippets.
- `explicit-waits.js` and `stable-selectors.js` export small helpers — call them from your tests or adapt the pattern inside your page objects.
- `playwright-ci.config.ts` exports a `ciProject` object; spread it into the `projects` array of your `playwright.config.ts`.
- `shard-ci.sh` assumes a GitHub Actions matrix with `shard` (1..4) and `total` (4) values.

No other dependencies.
