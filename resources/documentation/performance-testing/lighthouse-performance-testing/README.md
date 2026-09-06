# Lighthouse Performance Testing — Companion Scripts

Companion scripts for the [Lighthouse Performance Testing Guide](https://qapractices.com/documentation/lighthouse-performance-testing).

## Files

| File | Purpose |
| --- | --- |
| `scripts/lighthouserc.js` | Lighthouse CI 0.14 config with performance, accessibility and SEO thresholds. |
| `scripts/lighthouse-ci-workflow.yml` | GitHub Actions workflow that runs Lighthouse CI on every push. |
| `scripts/run-lighthouse-programmatic.js` | Node.js script that runs Lighthouse 12 programmatically and logs LCP, INP and performance score. |
| `scripts/web-vitals-collector.js` | Production RUM collector using the `web-vitals` 4 library. |
| `scripts/assert-lighthouse.js` | Assert script that fails a build if LCP exceeds 2500ms. |

## Usage

```bash
# Install dependencies
npm install -g lighthouse@12 @lhci/cli@0.14
npm install web-vitals@4 chrome-launcher lighthouse

# Run Lighthouse CI
lhci autorun --config=scripts/lighthouserc.js

# Run programmatic audit
node scripts/run-lighthouse-programmatic.js https://staging.qa.local

# Assert on a specific metric
node scripts/assert-lighthouse.js ./report.json
```

## Requirements

- Node.js 20+
- Lighthouse 12+
- Lighthouse CI 0.14+
- web-vitals 4+ (for RUM collector)
