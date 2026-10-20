# Dark Mode and Theme Switching Testing — Runnable Companion

Playwright 1.48+ spec covering the automatable parts of the [Dark Mode and Theme Switching Testing Checklist](https://qapractices.com/checklists/dark-mode-theme-switching-testing-checklist/): theme resolution order, persistence, FOIT detection, and toggle behavior.

## Contents

| File | Purpose |
|---|---|
| `dark-mode.spec.ts` | Theme resolution, FOIT, toggle and persistence tests |
| `meta.json` | Resource metadata |

## Requirements

- Node.js 20+
- `@playwright/test` 1.48+ (`npm i -D @playwright/test` and `npx playwright install chromium`)

## Usage

```bash
BASE_URL=https://your-app.com npx playwright test dark-mode.spec.ts --reporter=list
```

## Assumptions to adapt

The spec assumes three conventions — change them to match your app:

| Convention | Default | Where to change |
|---|---|---|
| Theme class on `<html>` | `dark` / `light` | `appliedTheme()` |
| Storage key | `localStorage['theme']` | `THEME_KEY` |
| Toggle accessible name | `/theme|modo|tema/i` | `getByRole('button', ...)` |

## What it does not cover

Contrast ratios, forced-colors mode, and third-party widget theming need manual review or dedicated tooling (axe-core, visual regression). The DOM-level assertions here complement, not replace, the visual pass in the checklist.

[Compañero en español](README.es.md)
