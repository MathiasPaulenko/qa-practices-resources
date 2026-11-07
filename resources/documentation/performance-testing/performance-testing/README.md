# Performance Testing Fundamentals — Runnable Examples

Companion code for [Performance Testing Fundamentals: Web Vitals and Budgets](https://qapractices.com/documentation/performance-testing/) ([es](https://qapractices.com/es/documentation/performance-testing/)).

## Contents

| File | What it does |
|---|---|
| `lighthouse-budget.json` | Performance budgets: resource sizes (script/image/document/font/stylesheet), third-party count, LCP and interactive timings |
| `check-budget.js` | Zero-dependency Node script that checks a Lighthouse JSON report against the budget and exits non-zero on breach |
| `sample-report.json` | Minimal Lighthouse-result-shaped report; intentionally breaches two budgets so you can see the failure output |
| `web-vitals-collector.js` | RUM collector for LCP/INP/CLS using `web-vitals` 5.x (`on*` API) with sendBeacon |
| `github-actions/perf.yml` | CI gate: Lighthouse CI with the budget, plus a no-token alternative using `check-budget.js` |

## Quick start

Check the sample report against the budget (no Lighthouse install needed):

```bash
node check-budget.js sample-report.json lighthouse-budget.json
```

Expected output — the sample breaches `size:script` (380 KB > 300) and `timing:largest-contentful-paint` (3100 ms > 2500):

```text
PASS  size:document                41 KB  (budget 50 KB)
FAIL  size:script                  380 KB  (budget 300 KB)
PASS  size:image                   402 KB  (budget 500 KB)
PASS  size:font                    86 KB   (budget 100 KB)
PASS  size:stylesheet              57 KB   (budget 60 KB)
PASS  count:third-party            3 items (budget 10 items)
FAIL  timing:largest-contentful-paint 3100 ms (budget 2500 ms)
PASS  timing:interactive           2800 ms (budget 3500 ms)

2 budget(s) breached.
```

Check a real report:

```bash
npx lighthouse https://staging.your-app.example --output=json --output-path=./report.json
node check-budget.js ./report.json ./lighthouse-budget.json
```

Requires Node 18+; no npm dependencies.

## web-vitals collector

```bash
npm install web-vitals@^5
```

Import `web-vitals-collector.js` from your app entry point and point `ENDPOINT` at your analytics collector.
