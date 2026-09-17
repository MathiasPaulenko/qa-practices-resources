# Writing BDD Scenarios with Cucumber — Runnable Examples

Companion resource for [BDD Scenarios with Cucumber: Gherkin Examples](https://qapractices.com/documentation/how-to-write-bdd-scenarios-cucumber/).

Three self-contained suites covering the same login feature, so you can compare the glue code:

- **Cucumber JVM 7.34.8** with JUnit Platform Suite
- **Behave 1.3.3** (Python)
- **@cucumber/cucumber 13.2.1** (JavaScript/Node)

Each suite demonstrates `Background`, `Scenario Outline` with `Examples`, a `Data Table` step, tag filtering (`@smoke`, `@regression`, `@wip`) and `@Before`/`@After` hooks. The step definitions delegate to a tiny in-memory `LoginPage`/`AuthService` fake — no browser, no external API, `mvn test` or `behave` just works.

## Scenario

A registered user logs in with email and password and lands on a dashboard. The outline covers valid credentials, wrong password, unknown user and empty email.

## Structure

```text
cucumber-jvm/    # Maven project, io.cucumber glue
behave/          # Python project, behave decorators
js/              # Node project, @cucumber/cucumber
```

## Prerequisites

- Java 17+ and Maven (for cucumber-jvm)
- Python 3.10+ (for behave)
- Node 20+ (for js)

## Run Cucumber JVM

```bash
cd cucumber-jvm
mvn test
```

## Run Behave

```bash
cd behave
pip install -r requirements.txt
behave
behave --tags @smoke
```

## Run JavaScript

```bash
cd js
npm install
npx cucumber-js
npx cucumber-js --tags @smoke
```

## Reports

- Java: `mvn test` writes `target/cucumber-reports.html`.
- JavaScript: `npx cucumber-js --format json:cucumber-report.json`, then feed it to `cucumber-html-reporter`.
- Behave: `behave -f json -o report.json` or `-f junit --junit-directory reports/` for CI.
