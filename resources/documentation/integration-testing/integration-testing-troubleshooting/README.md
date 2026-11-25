# Integration Testing Troubleshooting — Companion

Runnable files for the [Integration Testing Troubleshooting Guide](https://qapractices.com/documentation/integration-testing-troubleshooting).

## Files

| File | Purpose |
|------|---------|
| `js/nock-salesforce-stub.js` | nock 13.x stub for the Salesforce API — CI never touches the live endpoint |
| `js/rate-limited-caller.js` | Bottleneck 2.x throttled caller for unavoidable live calls |
| `js/transform-edge-cases.spec.js` | Jest specs covering null fields, UTC normalization and empty inputs in the transform layer |
| `docker/Dockerfile` | Pinned Node 20 Alpine test environment shared by local, CI and staging |
| `js/oauth-token-refresh.spec.js` | Client-credentials token refresh in `beforeAll` test setup |
| `js/parallel-safe-uuid-test.spec.js` | uuid 11.x namespaced test data with teardown — safe for parallel workers |

## Quick Start

```bash
# Node 20+ with Jest 29.x
npm install --save-dev jest nock bottleneck uuid
npx jest js/transform-edge-cases.spec.js js/parallel-safe-uuid-test.spec.js

# Build the pinned environment
docker build -f docker/Dockerfile -t integration-tests .
```

## Notes

- `nock-salesforce-stub.js` and `rate-limited-caller.js` export helpers — wire them into your own specs.
- `transform-edge-cases.spec.js` expects a `transform.js` exporting `transformStripeToSalesforce`; adapt the field names to your mapping.
- The OAuth spec uses `https://auth.staging.internal/oauth/token` as a placeholder — replace it with your provider's token endpoint and inject `API_CLIENT_ID`/`API_CLIENT_SECRET` via env vars.
