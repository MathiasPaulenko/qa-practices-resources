# Cartify Selenium 4 Interview Companion

This folder contains a runnable **Java/TestNG/Selenium 4** project that mirrors the Cartify checkout migration from the QAPractices guide [50 Selenium Interview Questions: The Cartify Selenium 4](https://qapractices.com/documentation/selenium-interview-questions/).

It is a small `cartify-checkout` project with Page Object Model classes, a retry analyzer, test data JSON, and a GitHub Actions workflow that runs the suite on Selenium Grid 4 with Chrome and Firefox nodes.

## Project structure

```text
cartify-checkout/
├── .github/
│   └── workflows/
│       └── test.yml
├── pom.xml
└── src/test/
    ├── java/com/cartify/
    │   ├── pages/
    │   │   ├── BasePage.java
    │   │   ├── LoginPage.java
    │   │   ├── CartPage.java
    │   │   ├── CheckoutPage.java
    │   │   └── PaymentPage.java
    │   ├── utils/
    │   │   └── RetryAnalyzer.java
    │   └── tests/
    │       ├── LoginTest.java
    │       └── CheckoutTest.java
    └── resources/
        ├── test-data.json
        └── log4j2.xml
```

## What it demonstrates

- `BasePage.java` provides `waitForPageLoad()`, explicit wait helpers, and screenshot capture on failure.
- `LoginPage.java`, `CartPage.java`, `CheckoutPage.java`, and `PaymentPage.java` implement the Page Object Model with CSS `[data-testid]` selectors.
- `RetryAnalyzer.java` implements TestNG `IRetryAnalyzer` with a max of 2 retries for flaky tests.
- `LoginTest.java` and `CheckoutTest.java` are TestNG test classes with `@DataProvider` reading from `test-data.json`.
- `pom.xml` pins Selenium 4.21.0, TestNG 7.10, Java 21, Allure 2.29, and ChromeDriver 124.
- `.github/workflows/test.yml` runs the suite on Selenium Grid 4 with Chrome and Firefox nodes via Docker Compose.
- `log4j2.xml` configures logging for debugging.

## Prerequisites

- Java 21 (JDK)
- Maven 3.9+
- Docker (for Selenium Grid 4)

## Run locally

```bash
cd cartify-checkout
mvn clean test
```

Expected output:

```text
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

## Run on Selenium Grid 4

Start a standalone Chrome node:

```bash
# Start a standalone Chrome node on port 4444 with Selenium 4.21.0
docker run -d -p 4444:4444 --shm-size="2g" selenium/standalone-chrome:4.21.0
```

Run tests against the Grid:

```bash
mvn clean test -Dgrid.url=http://localhost:4444
```

## Run on GitHub Actions

The workflow in `.github/workflows/test.yml` starts Selenium Grid 4 via Docker Compose, runs the TestNG suite, and uploads Allure reports as artifacts.

## Versions

| Dependency | Version |
|---|---|
| Selenium | 4.21.0 |
| TestNG | 7.10 |
| Java | 21 |
| Maven | 3.9 |
| Allure | 2.29 |
| ChromeDriver | 124 |

## Related guide

- [50 Selenium Interview Questions: The Cartify Selenium 4](https://qapractices.com/documentation/selenium-interview-questions/)
