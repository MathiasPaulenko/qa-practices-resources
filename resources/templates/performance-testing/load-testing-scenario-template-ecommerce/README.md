# Load Testing Scenario — E-commerce Checkout (companion)

Runnable companion for the [Load Testing Scenario template](https://qapractices.com/templates/load-testing-scenario-template-ecommerce).

## Contents

- `scripts/checkout-journey.js` — k6 script for the checkout journey (ramping-vus executor, journey-tagged thresholds, per-VU test users from `data/test-users.json`).
- `data/test-users.json` — user pool so VUs don't share a session (see the template's Negative Scenarios table).
- `scenario-config.json` — traffic profile, journey mix and thresholds mirroring the template's Sections 2, 4 and 6.

## Run

```bash
# baseline
k6 run -e BASE_URL=https://staging.your-app.internal scripts/checkout-journey.js

# spike override (0 -> 8500 VU in 30s)
k6 run -e BASE_URL=... --stage 30s:8500 --stage 10m:8500 --stage 30s:0 scripts/checkout-journey.js
```

Requirements: k6 0.55+. Point `BASE_URL` at a staging environment — never production, and use a payment sandbox.
