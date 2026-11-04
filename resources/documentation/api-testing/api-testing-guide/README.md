# API Testing Guide Companion

Companion resource for the [API Testing Guide: Practical Techniques](https://qapractices.com/documentation/api-testing-guide). Contains a Maven project with REST Assured 5.4.0, JUnit 5.10.2, Hamcrest 2.2, and JSON schema validation against an OpenAPI-derived schema.

## Files

| File | Purpose |
|------|---------|
| `pom.xml` | Maven configuration with REST Assured 5.4.0, json-schema-validator 5.4.0, JUnit 5.10.2, Hamcrest 2.2 |
| `src/test/java/com/qapractices/UsersApiContractTest.java` | Contract test: schema validation plus negative checks (401, 404) |
| `src/test/resources/schemas/users.json` | JSON Schema for the `/api/v1/users` list response |

## Quick Start

```bash
export API_BASE_URL=https://staging.qapractices.com
export STAGING_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
mvn clean test
```

## Requirements

- Java 17+
- Maven 3.9+
- A reachable API base URL (defaults to `https://staging.qapractices.com`, override with `API_BASE_URL`)
- A valid bearer token for protected endpoints (`STAGING_TOKEN`)

## Notes

- `users.json` is derived from the OpenAPI 3.0 specification of the users endpoint. Regenerate it when the contract changes.
- Negative tests assert the error contract (`401` for invalid tokens, `404` for missing resources). Adjust expected codes if your API documents different behavior.
- For local development without a real backend, point `API_BASE_URL` at a WireMock 3.x or MockServer instance serving the same contract.
