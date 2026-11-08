# Rate Limiting & Throttling Testing Checklist — Companion

Runnable scripts for the [Rate Throttling & Limiting Checklist](https://qapractices.com/checklists/rate-limiting-throttling-testing-checklist/) on QAPractices.

## Scripts

### `scripts/provoke-429.sh`

Bursts an endpoint until it rejects, then reports **which request hit the wall**. The boundary is what matters — request N passing and N+1 getting 429 is the off-by-one check most rate limiters fail. Fails on any 5xx (the limiter should reject, not break) and on no-429 bursts.

```bash
./scripts/provoke-429.sh https://api.acme-corp.test/search 30
```

### `scripts/verify-rate-limit-headers.sh`

Exhausts the limit, then inspects the rejecting response for `Retry-After` and the `X-RateLimit-*` trio. A 429 without `Retry-After` leaves clients hammering blindly — this fails until all four headers show up.

```bash
./scripts/verify-rate-limit-headers.sh https://api.acme-corp.test/search 30
```

## Requirements

- `bash`, `curl`

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Checks pass |
| 1 | Usage error or endpoint unreachable |
| 2 | Verification failed — no 429, 5xx instead of 429, or missing headers |
