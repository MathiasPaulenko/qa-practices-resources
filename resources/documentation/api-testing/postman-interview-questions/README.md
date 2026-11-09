# Top 20 Postman Interview Questions — Companion Resources

Companion resources for the [Top 20 Postman Interview Questions: FinFlow Payments API](https://qapractices.com/documentation/postman-interview-questions/) guide on QAPractices.com.

The files reproduce the FinFlow scenario used throughout the guide: a `FinFlow-Payments-v3` collection with `Auth`, `Payments`, `Refunds` and `Webhooks` folders, a collection-level pre-request script that computes the `X-Request-Signature` HMAC header, a staging environment, and the data files referenced by the Newman and data-driven questions.

## Contents

| File | Description |
| --- | --- |
| `collections/FinFlow-Payments-v3.json` | Postman v2.1 collection: 4 folders, chained requests (`login → createPayment → getPayment → createRefund`), `pm.test` assertions on status, `processorCode`, `idempotency_key`, `retryCount` and the 600 ms SLA. |
| `environments/staging.json` | Staging environment with `base_url`, `api_key`, `auth_token`, `token_expiry` and `correlation_id`. Fictional `*.finflow.example` domains — point them at your own mock or staging API. |
| `data/payments-test-data.csv` | 120 rows of payment data for Newman `-d` runs: valid payments, invalid currencies, expired tokens and duplicate `idempotency_key` cases. |
| `data/refunds-edge-cases.json` | Refund retry edge cases matching the staging regression case study (expired `correlation_id`, negative amounts, retries). |
| `.github/workflows/api-tests.yml` | GitHub Actions workflow that installs Newman 6 and gates pull requests against `staging`. |

## Requirements

- Postman v11 (GUI) or Newman 6.x (CLI)
- Node.js 20 LTS

## Quick Start

Import the collection and environment into Postman:

1. Open Postman v11
2. Click **Import** and select `collections/FinFlow-Payments-v3.json`
3. Click **Import** again and select `environments/staging.json`
4. Select the **FinFlow Staging** environment from the dropdown
5. Set `merchant_secret` as a collection variable (a placeholder value ships in the collection)
6. Run **Auth > POST /auth/login** first so the test script stores `auth_token`

## Run with Newman (CLI)

```bash
# Install Newman 6.x
npm install -g newman@6
npm install -g newman-reporter-htmlextra

# Full data-driven run (120 iterations)
newman run collections/FinFlow-Payments-v3.json \
  -e environments/staging.json \
  -d data/payments-test-data.csv \
  --reporters cli,junit,htmlextra

# Refunds folder only, edge cases — the case-study command
newman run collections/FinFlow-Payments-v3.json \
  -e environments/staging.json \
  -d data/refunds-edge-cases.json \
  --folder Refunds
```

> **Note:** the `*.finflow.example` URLs are placeholders. To see real responses, run the collection against a local mock (e.g. `json-server` or a Postman mock server) and update `base_url` in `environments/staging.json`.

## CI/CD Integration (GitHub Actions)

`.github/workflows/api-tests.yml` runs on every PR against `staging` and nightly at 03:00 UTC: it installs Newman 6, executes the full data-driven run, exports JUnit + htmlextra reports and uploads them as artifacts. Copy it into your repo's `.github/workflows/` folder.

## Related Resources

- [Top 20 Postman Interview Questions: FinFlow Payments API](https://qapractices.com/documentation/postman-interview-questions/)
- [How to Test REST APIs with Postman](https://qapractices.com/documentation/how-to-test-rest-api-postman/)
- [API Testing Guide](https://qapractices.com/documentation/api-testing-guide/)
