# API Testing Troubleshooting — Companion Snippets

Runnable code from the [API Testing Troubleshooting Guide](https://qapractices.com/documentation/api-testing-troubleshooting/).

| File | Purpose | Tool |
|---|---|---|
| `test-isolation.js` | Each test creates and cleans up its own data (fixes flaky state-dependent tests) | supertest 7 |
| `schema-validation.js` | Validates a payment response against the OpenAPI-derived JSON schema | Ajv 8 |
| `k6-perf-test.js` | Load test with SLA thresholds (p95 < 200ms, p99 < 500ms) | k6 0.54 |

## Usage

```bash
# Jest / Vitest examples
npm i supertest@7 ajv@8
npx jest test-isolation.js

# k6
k6 run -e API_TOKEN=your-token k6-perf-test.js
```
