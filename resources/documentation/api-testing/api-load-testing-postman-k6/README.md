# API Load Testing with Postman & k6 — Companion

This companion provides runnable files for the [API Load Testing with Postman & k6](https://qapractices.com/documentation/api-load-testing-postman-k6) guide.

## Files

| File | Purpose |
|------|---------|
| `test-plans/checkout-load.js` | k6 v2.x load test script for an e-commerce checkout flow |
| `test-plans/api-collection.json` | Postman collection with smoke tests for cart and checkout endpoints |
| `test-data/users.csv` | CSV data set with 10 test users for Newman iteration |
| `test-data/users.json` | JSON data set for k6 SharedArray |
| `scripts/assert-sla.py` | Python script to assert p95 and error rate from k6 JSON output |
| `.github/workflows/load-test.yml` | GitHub Actions workflow running k6 nightly |

## Quick Start

```bash
# Run the k6 load test locally
k6 run test-plans/checkout-load.js

# Run the Postman smoke test with Newman
newman run test-plans/api-collection.json -d test-data/users.csv -n 100

# Assert SLA from k6 JSON output
python scripts/assert-sla.py results.json
```

## CI Integration

The included GitHub Actions workflow runs the k6 load test nightly and uploads results as an artifact.