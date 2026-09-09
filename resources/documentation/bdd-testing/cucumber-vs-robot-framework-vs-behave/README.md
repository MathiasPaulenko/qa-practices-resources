# Cucumber vs Robot Framework vs Behave — Login Example

Companion resource for [Cucumber vs Robot Framework vs Behave: BDD Tool Comparison](https://qapractices.com/documentation/cucumber-vs-robot-framework-vs-behave/).

Three BDD suites testing the same API login scenario:

- **Cucumber JVM 7.34.3** with REST Assured 5.5.0
- **Robot Framework 7.4.2** with RequestsLibrary 0.9.7
- **Behave 1.3.3** with requests 2.32.3

## Scenario

A user with email `qa@qapractices.com` and password `ValidPass!2026` logs in through a local API at `http://127.0.0.1:8080`, receives a token, and reaches a dashboard that says `Welcome to QA Practices`.

## Structure

```text
cucumber-jvm/        # Maven project with Cucumber + REST Assured
robot-framework/     # Robot Framework with RequestsLibrary
behave/              # Behave with requests
.github/workflows/   # CI workflow running all three suites
```

## Prerequisites

- Java 17+ (for Cucumber JVM)
- Python 3.12+ (for Robot Framework and Behave)
- A running API at `http://127.0.0.1:8080` with endpoints:
  - `POST /api/v1/test-users` — create test user
  - `POST /api/v1/auth/login` — login, returns token
  - `GET /api/v1/dashboard` — protected dashboard

## Run Cucumber JVM

```bash
cd cucumber-jvm
mvn test -Dtest=RunCucumberTest
```

## Run Robot Framework

```bash
cd robot-framework
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
robot --variable BASE_URL:http://127.0.0.1:8080 tests/login.robot
```

## Run Behave

```bash
cd behave
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
behave features/login.feature
```

## CI

The workflow in `.github/workflows/bdd-comparison.yml` runs all three suites in GitHub Actions.

## Versions

| Tool | Version |
| --- | --- |
| Cucumber JVM | 7.34.3 |
| REST Assured | 5.5.0 |
| JUnit Platform | 1.14.2 |
| Robot Framework | 7.4.2 |
| robotframework-requests | 0.9.7 |
| Behave | 1.3.3 |
| requests | 2.32.3 |
