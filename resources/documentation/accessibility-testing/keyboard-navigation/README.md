# Keyboard Navigation Testing — Runnable Playwright Suite

Companion repository for the QAPractices guide
[Keyboard Navigation Testing Guide](https://qapractices.com/documentation/keyboard-navigation/)
([versión en español](https://qapractices.com/es/documentation/keyboard-navigation/)).

Self-contained: every fixture renders inline with `page.setContent()` — no
external site or backend required.

## Layout

```text
playwright/   @playwright/test 1.48.2
```

## Run

```bash
cd playwright
npm install
npx playwright test
```

The config uses `channel: 'chrome'` — it runs your installed Chrome, so no
browser download is needed. For CI, remove the channel option and run
`npx playwright install chromium` to use the bundled browser.

## What the suite covers

- **Tab order follows DOM order** — baseline expectation.
- **Positive `tabindex` reorders focus** — the anti-pattern to catch in review.
- **Modal focus trap** — Enter opens, Tab/Shift+Tab cycle inside, Escape
  closes and returns focus to the trigger.
- **Off-screen focusable links** — `left:-9999px` keeps them reachable by Tab;
  demonstrates a real-world keyboard bug.
- **Skip link** — first Tab stop, activates to move focus to `main`.

All five tests pass on Chrome stable with Playwright 1.48.
