# Dark Mode and Theme Switching Test Cases — Companion

Companion resource for [Dark Mode and Theme Switching Test Cases](https://qapractices.com/test-cases/dark-mode-theme-test-cases/).

## Contents

- `theme.mjs` — dependency-free theme-resolution model: stored preference → `prefers-color-scheme` → app default, with corrupted stored values falling back instead of throwing. `ThemeStore` wraps a shared `Map` so persistence and cross-tab behavior are testable without a browser.
- `contrast.mjs` — WCAG 2.2 contrast math (sRGB → relative luminance → contrast ratio) for the SC 1.4.3 and SC 1.4.11 assertions.
- `scan-hardcoded.mjs` — finds hex literals assigned to real CSS properties, i.e. colors that bypass the token system and stay identical across themes.
- `tests/dark-mode.test.mjs` — executable subset of the article's cases: system preference on first visit (TC-001), stored-beats-system (TC-002), persistence (TC-003), corrupted-value fallback (TC-006), token coverage + hardcoded-hex scan (TC-007), contrast AA in both themes (TC-008), focus-ring 3:1 (TC-009), dark elevation ordering (TC-011), live OS sync without manual override (TC-014) and cross-tab storage sync (TC-015).

## Requirements

- Node.js 20+ (uses the built-in `node:test` runner — no npm install needed)

## Usage

```bash
node --test tests/*.test.mjs
```

Expected output: `15 passed`.

The browser-level cases (TC-004 toggle, TC-005 FOIT, TC-010 media, TC-012 print, TC-013 embeds, TC-016 forced-colors) run as Playwright/Manual checks per the article — the spec in the article body covers the toggle assertion.

## Related

- Article EN: https://qapractices.com/test-cases/dark-mode-theme-test-cases/
- Article ES: https://qapractices.com/es/test-cases/dark-mode-theme-test-cases/
- Sibling checklist companion: [dark-mode-theme-switching-testing-checklist](../../checklists/quality-assurance/dark-mode-theme-switching-testing-checklist) (Playwright spec for resolution/FOIT/toggle)
