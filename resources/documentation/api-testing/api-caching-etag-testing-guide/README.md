# API Caching & ETag Guide — Companion

This companion provides runnable files for the [API Caching & ETag Guide](https://qapractices.com/documentation/api-caching-etag-testing-guide) guide.

## Files

| File | Purpose |
|------|---------|
| `tests/test_caching_etag.py` | Python requests test for ETag match, mismatch and mutation |
| `tests/k6_cache_hit_ratio.js` | k6 load test for cache hit ratio with thresholds |
| `scripts/etag_conditional.sh` | curl shell script for ETag and Last-Modified conditional requests |
| `scripts/cdn_validation.sh` | curl shell script for CDN cache validation |

## Quick Start

```bash
# Run Python tests
pip install requests pytest
pytest tests/test_caching_etag.py -v

# Run k6 load test
k6 run tests/k6_cache_hit_ratio.js

# Run curl scripts
bash scripts/etag_conditional.sh
bash scripts/cdn_validation.sh
```

## CI Integration

The Python tests can run in GitHub Actions with `pytest`. The k6 script can run in CI with `k6 run`.