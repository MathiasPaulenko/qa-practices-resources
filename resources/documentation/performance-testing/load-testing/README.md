# Load Testing — Runnable Examples

Runnable versions of the three examples from the article
[Load Testing Guide: Practical Techniques](https://qapractices.com/documentation/load-testing/).

## Contents

| File | What it does |
|---|---|
| `load-test.js` | Full k6 ramp profile: 5 stages (ramp-up, steady, ramp-up, steady, ramp-down) with `http_req_duration` and `http_req_failed` thresholds that fail the run. Target URL via `BASE_URL` env var. |
| `run-jmeter.sh` | Apache JMeter 5.6.x non-GUI runner: executes a `.jmx` plan, writes `results.jtl` and an HTML report. |
| `github-actions/k6-smoke.yml` | GitHub Actions job running a 60-second, 20-VU k6 smoke load inside the official `grafana/k6` Docker image on every PR. |

## Usage

```bash
k6 run -e BASE_URL=https://staging.example.com load-test.js
./run-jmeter.sh load-test-plan.jmx report/
```

For the GitHub Actions job, copy `github-actions/k6-smoke.yml` into
`.github/workflows/` in your repository and point the URL at your staging
environment. Keep the smoke run under two minutes — its job is catching
catastrophic regressions, not measuring capacity.

## Requirements

- k6 2.x — `brew install k6` / `winget install k6` or the `grafana/k6` Docker image
- Apache JMeter 5.6.x for `run-jmeter.sh`
- Docker (for the CI smoke job and for running k6 containerized)
