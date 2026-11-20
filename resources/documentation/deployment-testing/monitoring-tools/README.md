# Monitoring Tools Guide — Companion Scripts

Runnable companion for the [Monitoring Tools Guide](https://qapractices.com/documentation/monitoring-tools/) on QAPractices.

## Contents

| File | What it does |
|---|---|
| `scripts/prometheus-instrumentation.py` | Minimal `prometheus_client` 0.26.0 app that exposes `/metrics` with a counter and histogram, plus simulated traffic so dashboards actually move. |
| `scripts/alert-rules.yml` | Prometheus alerting rules implementing the P1-P4 severity matrix from the guide (error rate, latency, disk, scrape flapping). |
| `scripts/otel-node-setup.js` | OpenTelemetry tracing bootstrap for Node.js using the OTLP exporter (`@opentelemetry/sdk-node` 0.301.2) — Jaeger listens on `:4318` since v1.35. |
| `scripts/synthetic-login-check.spec.ts` | Playwright synthetic health check of the login journey, with a latency budget and env-var credentials. Runs on a cron or inside Datadog Synthetics / k6. |

## Requirements

- Python 3.10+ — `pip install prometheus_client==0.26.0`
- Node.js 20+ — `npm i @opentelemetry/sdk-node@0.301.2 @opentelemetry/exporter-trace-otlp-http@0.301.2`
- `@playwright/test` 1.65.1 for the synthetic spec

## Usage

```bash
# Metrics endpoint with simulated traffic
python scripts/prometheus-instrumentation.py
curl http://localhost:8000/metrics

# Local Jaeger for traces
docker run -p 4318:4318 -p 16686:16686 jaegertracing/all-in-one:1.62
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318 node scripts/otel-node-setup.js

# Synthetic check against staging
SYNTH_URL=https://staging.example.internal SYNTH_USER=qa SYNTH_PASS=... \
  npx playwright test scripts/synthetic-login-check.spec.ts
```

Alert rules load via `rule_files: ["scripts/alert-rules.yml"]` inside `prometheus.yml`. Never point synthetic credentials at a real user account.
