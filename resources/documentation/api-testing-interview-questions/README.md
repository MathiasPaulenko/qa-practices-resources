# Nexus Payments API Testing Interview Companion

Runnable companion for the QAPractices guide [50 API Testing Interview Questions](https://qapractices.com/documentation/api-testing-interview-questions/).

## What's inside

This companion mirrors the Nexus Payments checkout `v3.2.5` scenario from the interview guide. It includes:

- **`nexus-api-tests/`** — Java 17 + REST Assured 5.4.0 + Maven 3.9 project with:
  - `CheckoutTest.java` — happy path, duplicate-charge (409), idempotency, rate-limit tests
  - `AuthTest.java` — JWT validation, expired token, BOLA tests
  - `ContractTest.java` — JSON Schema validation for checkout and user endpoints
  - `RetryAnalyzer.java` — exponential backoff for rate-limited endpoints
  - `checkout-schema.json` / `user-schema.json` — JSON Schema contracts
  - `test-config.properties` — environment configuration
- **`postman/`** — Postman v11 collection + environment:
  - `nexus-checkout-smoke.json` — smoke collection (must finish < 180s)
  - `nexus-qa-env.json` — QA environment variables
- **`.github/workflows/api-smoke.yml`** — GitHub Actions workflow running Newman smoke on every PR

## Stack versions

| Tool | Version |
| --- | --- |
| Java | 17 |
| REST Assured | 5.4.0 |
| Maven | 3.9 |
| Postman | v11.0.11 |
| Newman | 6.1.2 |
| JUnit | 5.10.2 |
| GitHub Actions | latest |

## Running the Java tests

```bash
cd nexus-api-tests
mvn clean test -Denv=qa
```

## Running the Postman smoke

```bash
cd postman
newman run nexus-checkout-smoke.json -e nexus-qa-env.json --reporters cli,junit --reporter-junit-export results.xml
```

## The 409 incident

The `CheckoutTest.duplicateChargeReturns409()` test reproduces the incident from the guide: `POST /v2/checkout` with the same `Stripe-Idempotency-Key` twice should result in one charge, not two. The test asserts `409 Conflict` on the second call.

## License

MIT — see the main repo for details.
