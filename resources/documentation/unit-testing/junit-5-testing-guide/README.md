# JUnit 5 Testing Guide — Companion

Companion resource for [JUnit 5 Testing Guide for Java Developers](https://qapractices.com/documentation/junit-5-testing-guide).

## Contents

- `src/Calculator.java` — Domain class used in test examples
- `src/CalculatorTest.java` — Basic test with `@BeforeEach`, `@DisplayName`, assertions
- `src/ParameterizedTestExample.java` — `@ParameterizedTest` with `@ValueSource`, `@MethodSource`, `@CsvSource`
- `src/UserServiceTest.java` — `@Nested` test classes for context grouping
- `src/TimingExtension.java` — Custom `@ExtendWith` extension for test timing

## Requirements

- Java 17+
- JUnit 5.11+ (Jupiter)

## Usage

These are reference snippets, not a runnable Maven project. Copy the test classes into your project and add the JUnit 5 dependency:

```xml
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.11.0</version>
    <scope>test</scope>
</dependency>
```

See the guide for the full setup with Maven Surefire configuration.
