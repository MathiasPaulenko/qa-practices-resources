# API Latency & Throughput — Runnable Companion

Runnable scripts for the [API Latency & Throughput Test Cases](https://qapractices.com/test-cases/api-latency-throughput-test-cases/) on QAPractices.

## Contents

| File | Purpose |
|---|---|
| `k6-latency.js` | Concurrent load profile (TC-02/TC-03) with a `p(95)<500` threshold. |
| `k6-throughput-ramp.js` | Arrival-rate saturation ramp for finding the throughput ceiling (TC-02). |
| `jmeter-throughput-assertions.xml` | JMeter Throughput Controller + Duration Assertion fragment to embed in a test plan. |
| `latency-throughput.feature` | Gherkin scenarios for SLA, saturation and rate-limiting behavior. |

## Usage

```bash
k6 run k6-latency.js
k6 run k6-throughput-ramp.js

# against your own environment
API_BASE_URL=https://staging.example.com k6 run k6-latency.js
```

Both scripts read `API_BASE_URL` (default: `https://api.example.com`, a placeholder — point it at your staging environment). The JMeter fragment embeds inside a Thread Group next to your HTTP Request sampler.

## Source

- Resource: <https://qapractices.com/test-cases/api-latency-throughput-test-cases/>
- Versión en español: [README.es.md](README.es.md)
