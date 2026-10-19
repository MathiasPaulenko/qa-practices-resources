# Microservices Health Check Test Lab

Runnable companion for [Microservices Health Check Testing Checklist](https://qapractices.com/checklists/microservices-health-check-testing-checklist/) — a stdlib-only Python `HealthService` implementing the liveness/readiness/circuit-breaker/shutdown contract from the checklist, plus a pytest suite exercising the failure modes.

## Run

```bash
pip install -r requirements.txt
pytest -v
```

## What it covers

| Test | Checklist area |
|---|---|
| `test_liveness_ignores_dependencies` | Liveness never queries deps (restart-loop guard) |
| `test_liveness_fails_only_when_process_dead` | Liveness semantics |
| `test_readiness_503_on_critical_dep_down` | Critical dep → 503 |
| `test_readiness_200_on_noncritical_dep_down` | Non-critical dep → still ready |
| `test_readiness_logs_every_probe` | Probe observability |
| `test_breaker_opens_after_threshold` | Circuit opens after N failures |
| `test_open_breaker_short_circuits_calls` | Open circuit blocks calls |
| `test_half_open_closes_on_success` | Half-open recovery |
| `test_open_critical_breaker_degrades_readiness` | Breaker state feeds readiness |
| `test_sigterm_flips_readiness_but_not_liveness` | Graceful shutdown contract |
| `test_inflight_drains_before_exit` | In-flight drain |
| `test_shutdown_does_not_outlive_grace` | Hard kill at deadline |
| `test_aggregate_*` | Gateway health aggregation |
