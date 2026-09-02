# k6 Load Testing Companion

Runnable k6 v0.56 load test scripts for the [Load Testing with k6 guide](https://qapractices.com/documentation/load-testing-with-k6/).

## Requirements

- [k6 v0.56](https://k6.io/docs/get-started/installation/) or later
- Node.js 18+ (for any pre-processing scripts)
- A staging API to test against

## Files

| File | Description |
| --- | --- |
| `api-load.js` | Main load test script with login + order search flow, custom metrics and thresholds |
| `smoke-test.js` | Short low-load smoke test (5 VUs, 1 min) |
| `stress-test.js` | Ramp 0 to 400 VUs to find the breaking point |
| `spike-test.js` | Jump to 1000 VUs in 10s, hold 1 min, ramp down |
| `soak-test.js` | 100 rps for 4 hours to catch memory leaks |
| `data/users.json` | Sample user data for parameterized requests |
| `.github/workflows/k6-load.yml` | GitHub Actions workflow for CI integration |

## Quick start

```bash
# Install k6 (macOS)
brew install k6

# Install k6 (Windows)
choco install k6

# Run the main load test
k6 run api-load.js

# Run against a different environment
BASE_URL=https://staging-02.qapractices.com/api/v1 k6 run api-load.js

# Run smoke test
k6 run smoke-test.js

# Run in Docker
docker run --rm -v $(pwd):/scripts -w /scripts grafana/k6:2.2.0 run api-load.js

# Run in k6 Cloud
k6 cloud run api-load.js
```

## Environment variables

| Variable | Default | Description |
| --- | --- | --- |
| `BASE_URL` | `https://staging.qapractices.com/api/v1` | Target API base URL |
| `USER` | `qa-load@qapractices.com` | Login email |
| `PASS` | `Str0ngP@ss!` | Login password |
| `API_TOKEN` | (none) | Pre-generated token for custom metrics script |

## CI/CD

The included GitHub Actions workflow runs a smoke test on every push to `main` and on weekdays at 5 AM UTC. See `.github/workflows/k6-load.yml`.

## Source

This companion is part of the [QAPractices](https://qapractices.com) resource: [Load Testing with k6: Scenarios, Metrics and k6 Cloud](https://qapractices.com/documentation/load-testing-with-k6/).
