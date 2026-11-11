# Performance Testing Interview Questions Companion

Runnable load test assets for the [30 Performance Testing Interview Questions](https://qapractices.com/documentation/performance-testing-interview-questions/) guide.

## Requirements

- [k6 v0.56](https://k6.io/docs/get-started/installation/) or later
- [Apache JMeter 5.6.x](https://jmeter.apache.org/download_jmeter.cgi) (for the CI runner only)
- A staging API to point `BASE_URL` at

## Files

| File | Description |
| --- | --- |
| `interview-load-test.js` | k6 script combining staged ramp-up, p95/p99 and error-rate thresholds, and a SharedArray login flow fed by CSV |
| `data/users.csv` | Sample credentials consumed by the k6 script — replace with real staging users |
| `jmeter-ci.sh` | Non-GUI JMeter runner for CI/CD: produces `.jtl` results plus an HTML report folder |

## Quick start

```bash
# Run the k6 scenario against your staging API
BASE_URL=https://staging.example.internal k6 run interview-load-test.js

# Run a JMeter plan headless with HTML report
./jmeter-ci.sh my-plan.jmx
```

## What each file demonstrates

- **Stages and thresholds** — the script ramps to 20 virtual users over 30 seconds, holds one minute, and fails the run when `p(95)` exceeds 500ms or the error rate passes 1%, matching Q19 and Q27 of the guide.
- **Parameterization** — `SharedArray` loads `data/users.csv` once and hands each virtual user a unique row via `__VU`, matching Q20.
- **Correlation** — the login request runs first so a token can be extracted and reused, matching Q11 and Q29.
- **CI execution** — `jmeter-ci.sh` wraps `jmeter -n -t plan -l results -e -o report`, matching Q15.
