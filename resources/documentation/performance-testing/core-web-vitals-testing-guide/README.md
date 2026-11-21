# Core Web Vitals Testing — Lighthouse CI + RUM Snippets

Companion to [Core Web Vitals Testing Guide: Lab, Field, and CI/CD Tools](https://qapractices.com/documentation/core-web-vitals-testing-guide/).

A minimal, runnable CWV gate: Lighthouse CI asserts LCP and CLS budgets on every pull request, and the `web-vitals` snippet ships real-user metrics from production.

## Files

```text
lighthouserc.json    # @lhci/cli 0.16 config: URLs, 3 runs, LCP/CLS/TBT assertions
lighthouse-ci.yml    # GitHub Actions workflow running `lhci autorun` on PRs
cwv-report.js        # web-vitals 6.x RUM collector (onLCP/onINP/onCLS)
```

## Quick start

```bash
npm install -D @lhci/cli@0.16.0
# Point lighthouserc.json at your staging/preview URLs first (placeholders)
npx lhci autorun
```

For GitHub Actions: copy `lighthouse-ci.yml` to `.github/workflows/` and set the `LHCI_GITHUB_APP_TOKEN` secret, or drop the env block to skip status comments.

For RUM: bundle `cwv-report.js` (npm `web-vitals@^6`) and point `sendBeacon` at your own analytics endpoint — `/rum` in the snippet is a placeholder route.

## Versions

- @lhci/cli: 0.16.x
- Lighthouse: 12.x (bundled with @lhci/cli)
- web-vitals: 6.x
- Node.js: 20 (GitHub Actions)
