# API Gateway Guide — Companion

This companion provides runnable files for the [API Gateway Guide](https://qapractices.com/documentation/api-gateway-testing-guide) guide.

## Files

| File | Purpose |
|------|---------|
| `scripts/route_validation.sh` | curl script to test exact, prefix, host-based and method-restricted routes |
| `scripts/rate_limit_test.sh` | curl script to test rate limiting thresholds and response headers |
| `scripts/tls_validation.sh` | curl script to validate TLS versions, certificates and security headers |
| `tests/k6_gateway_load_test.js` | k6 load test through the gateway with ramp-up stages and thresholds |

## Quick Start

```bash
# Run route validation
bash scripts/route_validation.sh

# Run rate limit test
bash scripts/rate_limit_test.sh

# Run TLS validation
bash scripts/tls_validation.sh

# Run k6 load test
k6 run tests/k6_gateway_load_test.js
```