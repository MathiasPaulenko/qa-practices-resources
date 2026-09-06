# Playwright Visual Regression Testing — Companion

Companion files for the [Playwright Visual Regression Testing guide](https://qapractices.com/documentation/playwright-visual-regression-testing).

## Files

| File | Purpose |
| --- | --- |
| `playwright.config.js` | Playwright config with snapshotPathTemplate, toHaveScreenshot defaults and 3 viewport projects. |
| `tests/visual-homepage.spec.js` | Full-page visual regression test for homepage. |
| `tests/visual-checkout.spec.js` | Component-level visual test for checkout summary with API mock and mask. |
| `tests/visual-button.spec.js` | Component-level visual test for a primary button in Storybook. |
| `.github/workflows/visual-regression-tests.yml` | GitHub Actions workflow to run visual tests in CI. |

## Requirements

- Node.js 20+
- Playwright 1.48+

## Usage

1. Copy `playwright.config.js` to your project root.
2. Copy the test files to your `tests/` directory.
3. Copy the GitHub Actions workflow to `.github/workflows/`.
4. Run `npx playwright install --with-deps` to install browsers.
5. Run `npx playwright test` to execute visual tests.
6. On first run, baselines are generated. Review and commit them.
7. On subsequent runs, Playwright compares against the stored baselines.

## Baseline Update

When a visual change is intentional:

```bash
npx playwright test --update-snapshots
```

Review the diff in `playwright-report/index.html` before committing the updated baselines.
