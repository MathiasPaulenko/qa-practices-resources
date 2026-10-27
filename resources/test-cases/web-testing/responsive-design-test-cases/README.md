# Responsive Design Test Cases — Playwright companion

Companion for [Responsive Design Test Cases: Breakpoints, Viewport](https://qapractices.com/test-cases/responsive-design-test-cases/).

- `responsive-fixture.html` — a page with a real 768px breakpoint: `.hamburger` button below, `.desktop-nav` above, plus an 8-column table inside `overflow-x: auto`.
- `responsive.spec.ts` — Playwright 1.48 viewport-matrix spec covering TC-01/10 (nav collapse at N-1/N/N+1) and TC-05/06 (no body-level horizontal scroll at 320px).

## Run

```bash
npm install
npx playwright install chromium   # first time
npm test
```

All 7 tests pass as-is. Break the fixture on purpose — e.g., remove `overflow-x: auto` — and watch the scroll assertion fail (that's TC-06 catching a real bug).
