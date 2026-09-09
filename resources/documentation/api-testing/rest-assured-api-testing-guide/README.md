# REST Assured API Testing Guide Companion

Companion resource for the [REST Assured API Testing Guide](https://qapractices.com/documentation/rest-assured-api-testing-guide). Contains a Maven project with REST Assured 5.4.0, JUnit 5.10.2, Hamcrest 2.2, JSON schema validation, and a GitHub Actions CI workflow.

## Files

| File | Purpose |
|------|---------|
| `pom.xml` | Maven configuration with REST Assured 5.4.0, JUnit 5.10.2, Hamcrest 2.2 |
| `src/test/java/com/qapractices/UserCrudTest.java` | CRUD test class with ordered execution |
| `src/test/java/com/qapractices/AuthTest.java` | Authentication tests (Basic, Bearer, OAuth2, API Key) |
| `src/test/resources/schemas/user-schema.json` | JSON Schema for user response validation |
| `.github/workflows/api-tests.yml` | CI workflow that runs `mvn clean test` on push/PR |

## Quick Start

```bash
mvn clean test
```

## Requirements

- Java 17+
- Maven 3.9+
- Internet access (tests run against https://reqres.in)
