# Results Analysis Checklist

What to check in the JTL/HTML report after a non-GUI run:

| Check | Where | Healthy | Action if failed |
|---|---|---|---|
| Error rate | Summary Report | < 1% | read failure samples, check server logs |
| Avg response time | Aggregate Report | < 500ms (API) | profile slow endpoint, check DB |
| p90 / p99 | Percentiles graph | < 1s / < 2s | find the slow tail — usually 1-2 endpoints |
| Throughput | Summary Report | meets target rps | scale test up or find saturation point |
| Active users | Threads graph | = thread count | ramp-up too steep → increase ramp period |
| Errors by type | Results Tree | none unexpected | 500s = app bug; timeouts = capacity |

Rules of thumb:
- never trust a run where the injector machine was also the server
- discard the first 60s of samples — cold caches distort every metric
- a 200 with an error body is still a failure — assertions must check content
