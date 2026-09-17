# TestNG vs JUnit 5 — Companion

Companion resource for [TestNG vs JUnit 5: Which to Choose](https://qapractices.com/documentation/testng-vs-junit-5).

## Contents

- `src/LoginTests.java` — TestNG 7.10: `@DataProvider` + `@Test(dataProvider)` login test
- `src/DataProviderExample.java` — TestNG `@DataProvider` vs JUnit 5 `@ParameterizedTest`/`@CsvSource` side by side
- `src/DependencyTests.java` — TestNG `dependsOnMethods` for chained flows (login → dashboard → logout)
- `src/testng.xml` — TestNG suite config with `parallel="methods"` and group filtering
- `src/junit-platform.properties` — JUnit 5.11 parallel execution configuration

## Requirements

- Java 17+
- TestNG 7.10+
- JUnit 5.11+ (Jupiter)

## Usage

Reference snippets, not a runnable Maven project. Copy into your project and add the dependencies:

```xml
<dependency>
    <groupId>org.testng</groupId>
    <artifactId>testng</artifactId>
    <version>7.10.2</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.11.0</version>
    <scope>test</scope>
</dependency>
```

Both frameworks can coexist in the same Maven module — Surefire picks up each provider automatically. See the guide for the full migration example and decision criteria.
