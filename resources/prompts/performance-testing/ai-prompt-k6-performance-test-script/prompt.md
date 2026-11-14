You are a performance engineer with strong k6 experience (k6 1.x). Write one or more runnable k6 scripts for the system below. Before writing code, ask for any missing detail that would make the output invalid or unrealistic.

System details:
- Application type: [REST API / GraphQL / gRPC / WebSocket / web app / microservice]
- Base URL: [https://api.example.com]
- Authentication: [none / Bearer token / API key / OAuth2 / Basic auth / mTLS]
- Endpoints and workload mix: [list endpoints with relative traffic, e.g. GET /products 70%, POST /orders 20%, DELETE /cart 10%]
- Normal load: [VUs or RPS]
- Peak load: [VUs or RPS]
- SLAs: [p95 latency, p99 latency, max error rate]
- Test environment: [staging / production-like / isolated perf environment]
- CI/CD platform: [GitHub Actions / GitLab CI / Jenkins / Azure DevOps]
- Monitoring: [Grafana / Datadog / Prometheus / k6 Cloud / custom]
- Test data source: [static / CSV / generated / API]
- Think time: [none / 1s / 5s / variable]

For each requested test type, choose the right executor and set concrete VU, stage and duration values. Define thresholds from the stated SLAs, not aspirational numbers. Add setup() and teardown() when the script needs fresh tokens or test data.

Smoke test:
- A few VUs for about a minute to validate the script and the environment.
- Uses shared-iterations or constant-vus before any longer run.

Load test:
- Baseline, normal and peak stages; ramp VUs up and down, never slam the system.
- Use ramping-vus, or constant-arrival-rate / ramping-arrival-rate when RPS control matters more than concurrent users.
- Apply per-endpoint weights matching the workload mix; add think time between requests.

Stress test:
- Ramp VUs until error rate exceeds a threshold or latency degrades sharply.
- Continue slightly past the breakpoint to observe recovery behavior.
- Categorize failures: timeouts, 5xx, connection refused, OOM; document the breakpoint in VUs and RPS.

Spike test:
- Jump to a high VU count quickly, hold briefly, then drop to baseline.
- Measure recovery time and how autoscaling, circuit breakers and rate limits react.

Soak / endurance test:
- Run at normal load for several hours at constant-vus.
- Watch memory, connections, file descriptors and DB pool usage for leaks; look for cache hit-rate drift.

Breakpoint test:
- Increase load in fixed steps or binary-search the maximum sustainable throughput.
- Record the first component that saturates: CPU, memory, DB, network or connection pool.

Script structure and extras:
- Use options, scenarios and thresholds.
- Implement checks for business logic, not just HTTP status.
- Add custom metrics (trend, counter, gauge, rate) for events the built-ins do not cover.
- Correlate requests: extract tokens, resource IDs and cookies; chain create -> read -> update -> delete.
- Read test data from CSV, JSON or SharedArray — never one hard-coded dataset for all VUs.
- Keep authentication setup in setup() or a reusable function.
- Save JSON and HTML results, fail CI builds on SLA breaches via thresholds, and export metrics to the configured backend.

For every script, provide:
- Test type and executor, VU count, duration and target RPS
- Endpoints, authentication setup, payloads and headers
- Thresholds for p95, p99 and error rate
- Custom metrics and business checks
- Expected behavior, failure criteria and CI/CD integration notes
