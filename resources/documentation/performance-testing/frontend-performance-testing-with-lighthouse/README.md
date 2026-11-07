# Frontend Performance Testing with Lighthouse — Runnable Examples

Runnable versions of the examples in [Frontend Performance Testing with Lighthouse: LCP, INP, CLS](https://qapractices.com/documentation/frontend-performance-testing-with-lighthouse/).

## Contents

| Path | What it does |
|---|---|
| `scripts/lighthouse-audit.js` | Runs Lighthouse 12 through Puppeteer 24 and prints the performance score plus the five weighted metrics. |
| `scripts/package.json` | Pinned dependencies: `lighthouse@12`, `puppeteer@24`. |
| `ci/lighthouserc.json` | Lighthouse CI 0.14 config: 3 runs per URL, performance ≥ 0.9, LCP ≤ 2500ms, CLS ≤ 0.1, TBT warning at 300ms. |
| `ci/lighthouse-ci.yml` | GitHub Actions workflow running `treosh/lighthouse-ci-action@v12` on pull requests. |

## Usage

```bash
cd scripts
npm install
npm run audit -- https://staging.example.com
```

For the CI gate, copy `ci/lighthouserc.json` into your repo, point `collect.url` at your preview environment, and place `ci/lighthouse-ci.yml` at `.github/workflows/lighthouse-ci.yml`.

## Notes

- `numberOfRuns: 3` reports the median per URL — a single run is too noisy to gate on.
- INP is a field metric and never appears in the lab score; assert `total-blocking-time` as its lab proxy.
- Tune the budgets to your own baseline before gating on `error`.
