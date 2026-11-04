# Performance and Load Test Cases — Runnable k6 Companion

Runnable k6 scenarios for
[Performance and Load Testing: 32 Test Cases](https://qapractices.com/test-cases/performance-load-testing-test-cases/)
([versión en español](https://qapractices.com/es/test-cases/performance-load-testing-test-cases/)).

| Script | Maps to | What it proves |
|---|---|---|
| `load-profile.js` | TC-PL-01, 04, 07 | Ramp-up/steady/spike/ramp-down with p95/p99 + error-rate thresholds |
| `capacity-arrival-rate.js` | TC-PL-18 | Constant arrival rate — sustained req/s, not just VU latency |
| `soak-test.js` | TC-PL-12 | 4h moderate hold to expose leaks and drift |

## Setup

Requires [k6](https://k6.io/) 0.55+. No npm install needed — k6 runs the scripts directly.

## Run

```bash
k6 run load-profile.js
BASE_URL=https://staging.example-shop.internal k6 run capacity-arrival-rate.js
k6 run soak-test.js
```

Set `BASE_URL` to point at your own service; the default hits `http://localhost:8080`.
A run without `thresholds` breaches still exits 0 in some setups — keep the
`thresholds` blocks so CI can catch regressions.
