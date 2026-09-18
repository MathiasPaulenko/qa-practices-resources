# TestNG Complete Guide — Companion

Companion resource for [TestNG Complete Guide: Parallel & Annotations](https://qapractices.com/documentation/testng-complete-guide).

Runnable Maven project with the examples from the guide: `CalculatorTest` with `@BeforeClass`/`@AfterClass` and `testName`, `LoginTest` with a `@DataProvider`, and a `testng.xml` suite with group filtering and parallel execution.

## Contents

- `src/main/java/com/qapractices/Calculator.java` — class under test (add, subtract, divide)
- `src/main/java/com/qapractices/AuthService.java` — minimal service for the data provider login test
- `src/test/java/com/qapractices/CalculatorTest.java` — TestNG 7.12 test with groups and `testName`
- `src/test/java/com/qapractices/LoginTest.java` — `@DataProvider` parameterized login test
- `src/test/resources/testng.xml` — suite config with `parallel="methods"`, `thread-count="4"` and group filtering
- `pom.xml` — TestNG 7.12.0 + Surefire 3.2.5 wired to the suite file

## Requirements

- Java 17+
- Maven 3.9+

## Usage

```bash
mvn test                      # run the full suite (smoke + regression)
mvn test -Dgroups="smoke"     # run only the smoke group
mvn test -DexcludedGroups="regression"  # run everything except regression
```

See the guide for the annotation lifecycle, listeners, soft assertions and CI/CD setup.
