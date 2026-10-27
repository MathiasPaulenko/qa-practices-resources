# Accessibility Testing Test Cases — Playwright companion

Companion for [Accessibility Testing Test Cases: WCAG Examples](https://qapractices.com/test-cases/accessibility-testing-test-cases/).

- `fixture-modal.html` — a real, WCAG-correct focus-trap modal (TC-A11Y-012 pattern): focus moves in on open, Tab cycles inside, Escape closes and returns focus to the trigger.
- `a11y.spec.ts` — Playwright 1.48 + `@axe-core/playwright` 4.10 spec from the resource, pointed at the fixture via `file://` so no server is needed.

## Run

```bash
npm install
npx playwright install chromium   # first time
npm test
```

To verify a *broken* trap, delete the `keydown` handler in the fixture and watch the focus-leak assertion fail — that's TC-A11Y-002 catching a real bug.
