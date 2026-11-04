# API Security Testing Guide — Companion

This companion provides runnable files for the [API Security Testing Guide: OWASP Top 10](https://qapractices.com/documentation/api-security-testing) guide.

## Files

| File | Purpose |
|------|---------|
| `scripts/bola-idor-test.sh` | BOLA/IDOR probe: replays a request with a different resource ID, expects 403/404 |
| `scripts/jwt-tampering-test.sh` | Sends a token with an altered payload/invalid signature, expects 401 |
| `scripts/rate-limit-probe.sh` | Fires 100 rapid requests, expects 429 + Retry-After past the threshold |
| `scripts/zap-baseline.sh` | Runs the OWASP ZAP 2.15 baseline scan in Docker and writes an HTML report |

## Quick Start

```bash
# Set your environment first — never run against production
export BASE_URL="https://staging.example.com"
export USER_A_TOKEN="<test-user-token>"
export TAMPERED_TOKEN="<altered-token>"

bash scripts/bola-idor-test.sh
bash scripts/jwt-tampering-test.sh
bash scripts/rate-limit-probe.sh
bash scripts/zap-baseline.sh
```

## CI Integration

Run `bola-idor-test.sh` and `jwt-tampering-test.sh` on every deploy to staging; they are fast and deterministic. Keep `rate-limit-probe.sh` and `zap-baseline.sh` on a nightly schedule — they are noisy and slower.
