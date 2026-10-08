# Visual Regression Testing Guide — Companion

Runnable examples for the [Visual Regression Testing: Baseline & Screenshot Diff guide](https://qapractices.com/documentation/visual-regression-testing-guide). Each folder covers one tool so you can pick the stack that fits your team.

## Files

| File | Purpose |
| --- | --- |
| `tests/visual-baseline.spec.js` | Playwright `toHaveScreenshot` baselines with tolerance options and region masking. |
| `percy/percy-visual.spec.js` | Percy snapshots inside a Playwright test, run through `percy exec`. |
| `percy/.percy.yml` | Percy snapshot config: mobile + desktop widths, spinner suppression. |
| `backstopjs/backstop.json` | Self-hosted config: two viewports, scenario selectors, 0.1% mismatch threshold. |
| `applitools/applitools-eyes.spec.js` | Applitools Eyes with `ClassicRunner`, batch config and `closeAsync`. |
| `.github/workflows/visual-regression-tests.yml` | PR workflow that runs `@visual` tests and uploads diff artifacts on failure. |

## Requirements

- Node.js 20+
- `@playwright/test` 1.63+ (Playwright examples)
- `@percy/cli` 1.32+ and `@percy/playwright` 1.1+ (Percy example)
- `backstopjs` 6.3+ (BackstopJS example)
- `@applitools/eyes-playwright` 1.49+ and `APPLITOOLS_API_KEY` (Applitools example)

## Usage

### Playwright

1. Copy `tests/visual-baseline.spec.js` into your project's `tests/` folder.
2. Replace `BASE_URL` with your staging URL.
3. Run `npx playwright test` once to generate baselines, review them, and commit the PNGs.
4. Update baselines after intentional UI changes with `npx playwright test --update-snapshots`.

### Percy

1. Copy `percy/percy-visual.spec.js` and `percy/.percy.yml` into your project.
2. Export `PERCY_TOKEN` from your Percy project settings.
3. Run `npx percy exec -- playwright test percy/percy-visual.spec.js`.
4. Review and approve diffs in the Percy dashboard.

### BackstopJS

1. Copy `backstopjs/backstop.json` to your project root as `backstop.json`.
2. Run `npx backstop reference` to capture baselines, then `npx backstop test` to compare.
3. Approve reviewed changes with `npx backstop approve` and commit `backstop_data/`.

### Applitools

1. Copy `applitools/applitools-eyes.spec.js` into your `tests/` folder.
2. Export `APPLITOOLS_API_KEY` as an environment variable or CI secret.
3. Run `npx playwright test applitools/applitools-eyes.spec.js` and review diffs in the Applitools dashboard.

### CI

Copy `.github/workflows/visual-regression-tests.yml` to your repo's `.github/workflows/`. Baselines must be generated on the same OS as the runner (`ubuntu-latest` here) or every run will diff on font rendering.

## Baseline Discipline

Never approve or regenerate a baseline without reviewing the diff first — that single habit is what separates visual testing from screenshot noise.
