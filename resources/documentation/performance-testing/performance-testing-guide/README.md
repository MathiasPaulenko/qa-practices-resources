# Performance Testing Guide — Companion

Companion files for [Performance Testing: Complete Guide to Types and Planning](https://qapractices.com/documentation/performance-testing-guide).

## Files

| File | Purpose |
| --- | --- |
| `product-load-test.js` | k6 load test: ramps to 100 VUs, steady state, p95 < 500ms and error rate < 1% thresholds. |

## Requirements

- k6 v0.51.0 (`k6 version`) or Docker for `grafana/k6:0.51.0`

## Usage

1. Point the script at your staging URL (replace `https://staging.qapractices.com/api/v1/products`).
2. Run locally: `k6 run product-load-test.js`.
3. Run in Docker: `docker run --rm -v $(pwd):/k6 grafana/k6:0.51.0 run /k6/product-load-test.js`.
4. Adjust `stages` and `thresholds` to your SLA before gating CI on the results.

## CI Integration

```yaml
- run: docker run --rm -v ${{ github.workspace }}:/k6 grafana/k6:0.51.0 run /k6/product-load-test.js
```
