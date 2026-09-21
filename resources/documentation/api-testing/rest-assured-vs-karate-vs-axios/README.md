# REST Assured vs Karate vs Axios Companion

Companion resource for the [REST Assured vs Karate vs Axios](https://qapractices.com/documentation/rest-assured-vs-karate-vs-axios) comparison. It implements the same scenario — `GET /users/1` plus a 404 negative path against [JSONPlaceholder](https://jsonplaceholder.typicode.com) — in all three libraries so you can compare syntax, setup cost, and output side by side.

## Files

| File | Purpose |
|------|---------|
| `rest-assured/pom.xml` | Maven config with REST Assured 5.5.7, JUnit 5.11.4, Hamcrest 3.0 |
| `rest-assured/src/test/java/com/qapractices/UserApiTest.java` | JUnit 5 test class with fluent DSL assertions |
| `karate/users-api.feature` | Gherkin scenarios using `match` assertions and `karate-config.js` |
| `karate/karate-config.js` | Environment config (`baseUrl` overridable with `-DbaseUrl=...`) |
| `axios/package.json` | Node project with Axios 1.20.x and Jest 30 |
| `axios/user-api.test.js` | Jest test with a shared Axios instance (`baseURL` + default headers) |

## Quick Start

### REST Assured

```bash
cd rest-assured
mvn clean test
```

Requires Java 17+ and Maven 3.9+.

### Karate

Download the standalone JAR from the [Karate releases page](https://github.com/karatelabs/karate/releases) and run:

```bash
java -jar karate.jar users-api.feature
```

Or embed the feature in a Maven/Gradle project with the `io.karatelabs:karate-junit5` dependency.

### Axios

```bash
cd axios
npm install
npm test
```

Requires Node.js 20+.

## What to compare

- **Lines of setup**: REST Assured needs a `pom.xml` and imports; Karate needs a feature file plus `karate-config.js`; Axios needs `npm install` and a test runner.
- **Assertion style**: fluent `.body(...)` matchers vs Karate `match` vs Jest `expect`.
- **Reporting**: REST Assured reports through Surefire/Allure, Karate generates HTML reports automatically, Axios tests report through Jest.
- **Parallelism**: Karate runs scenarios in parallel by default; the other two need runner-level configuration.
