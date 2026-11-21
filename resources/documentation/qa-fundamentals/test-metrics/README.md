# Test Metrics Quick Reference — Companion

Runnable snippets from the [Test Metrics Quick Reference: KPIs](https://qapractices.com/documentation/test-metrics/) guide on QAPractices.

## Contents

- `jest.config.js` — coverage threshold gate for Jest 30: CI fails if branch coverage drops below 70% or line/function/statement coverage below 80%.
- `scripts/defect_density.js` — ranks modules by defects per KLOC to find the hotspot worth investigating first. Run with `node scripts/defect_density.js`.
- `scripts/flaky_test_check.sh` — runs one Jest spec 10 times and counts failures, so you can quantify flakiness instead of guessing. Run with `./scripts/flaky_test_check.sh <path-to-spec>`.

## Requirements

- Node.js 20+ with Jest 30 installed in your project (`npm i -D jest`).
- Bash for the flake-check script (Git Bash works on Windows).
