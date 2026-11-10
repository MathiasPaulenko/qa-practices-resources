# Frontend Performance Testing — CI Budgets and RUM Examples

Companion to [Frontend Performance Testing: Metrics, Tools, Budgets](https://qapractices.com/documentation/frontend-performance-testing-guide/).

A minimal, runnable performance-budget gate: Lighthouse CI asserts Core Web Vitals on every pull request, and the `web-vitals` snippet ships real-user metrics from production.

## Files

```text
ci/
├── lighthouserc.json        # @lhci/cli 0.16 config: URLs, 3 runs, budget assertions
└── performance-budget.yml   # GitHub Actions workflow running `lhci autorun` on PRs
rum/
└── web-vitals.js            # web-vitals 6.x RUM collector (onLCP/onINP/onCLS/onFCP/onTTFB)
```

## Quick start

```bash
npm install -g @lhci/cli@0.16
# Point lighthouserc.json at your preview/staging URLs first
lhci autorun --config=ci/lighthouserc.json
```

For GitHub Actions: copy `ci/performance-budget.yml` to `.github/workflows/` and set the `LHCI_GITHUB_APP_TOKEN` secret (or drop the env block to skip status comments).

For RUM: bundle `rum/web-vitals.js` (npm `web-vitals@^6`) and point `sendBeacon` at your own analytics endpoint — `/rum` in the snippet is a placeholder route.

## Versions

| Piece | Version pinned |
|---|---|
| @lhci/cli | 0.16.x |
| Lighthouse (under lhci) | 13.x |
| web-vitals | 6.x (API `on*`; `get*`/`onFID` removed in v4/v5) |
| Node | 20+ |
