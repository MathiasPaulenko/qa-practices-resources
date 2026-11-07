# WCAG Accessibility Testing Guide — Runnable Examples

Companion code for [WCAG Accessibility Testing Guide](https://qapractices.com/documentation/accessibility-wcag-testing-guide/). Each example maps a WCAG 2.2 verification technique from the guide to a runnable check.

## Layout

| Path | What it covers |
|---|---|
| `playwright/tests/pour-rules.spec.js` | axe-core rules grouped by POUR principle — targeted scans instead of one giant pass |
| `playwright/tests/dom-checks.spec.js` | Two cheap DOM checks scanners miss: heading hierarchy and form-label association |
| `jest-axe/login-form.test.jsx` | Component-level jest-axe assertion inside a Jest + Testing Library suite |
| `ci/lighthouserc.js` | Lighthouse CI assertions gating the accessibility category |
| `ci/accessibility-tests.yml` | GitHub Actions job: axe CLI on critical pages + Lighthouse autorun |

## Run the Playwright specs

```bash
cd playwright
npm install
npx playwright test
```

Both specs hit `BASE_URL` (defaults to `http://localhost:3000`). Point it at a staging URL:

```bash
BASE_URL=https://staging.example.com npx playwright test
```

## Run the jest-axe test

```bash
cd jest-axe
npm install --save-dev jest @testing-library/react jest-axe@9
npx jest login-form.test.jsx
```

The spec expects a `LoginForm` component in scope — swap the import for a real component from your app.

## CI gate

Drop `ci/accessibility-tests.yml` into `.github/workflows/` and `ci/lighthouserc.js` at the repo root. The job scans three critical pages with `@axe-core/cli` and fails on any violation, then runs `lhci autorun` for the accessibility category score (≥0.95).

Scope the gate to WCAG 2.2 A/AA on critical flows first — a gate that fails on AAA or minor findings gets disabled within a sprint.
