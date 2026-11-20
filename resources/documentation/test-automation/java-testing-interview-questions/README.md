# Java Testing Interview Companion

Runnable versions of the answers in the QAPractices guide [Java Testing Interview: Spring & JUnit](https://qapractices.com/documentation/java-testing-interview-questions/) ([versión en español](https://qapractices.com/es/documentation/java-testing-interview-questions/)).

## What's inside

| File | Interview question it covers |
|---|---|
| `examples/LifecycleAndAssertionsTest.java` | Q4 lifecycle order, Q5 `@DisplayName`, Q6 assertions including `assertAll`, Q7 assumptions, Q17 `assertThrows` |
| `examples/ParameterizedExamplesTest.java` | Q8 `@ParameterizedTest` with `@ValueSource`, `@CsvSource`, `@MethodSource` |
| `examples/MockitoExamplesTest.java` | Q10 `when`/`verify` flow, Q11 mock vs spy side by side, Q12 argument matchers including `eq()` and `argThat()` |
| `examples/TestNgDataProviderTest.java` | Q9 TestNG `@DataProvider` running next to JUnit 5 |
| `examples/pom.xml` | Q15 Surefire 3.5.6 config with includes/excludes; JUnit 5.12.2, Mockito 5.14.2, TestNG 7.10.2 |

## Run it

Requires JDK 17+ and Maven 3.9+.

```bash
cd examples
mvn test
```

The suite mixes JUnit 5 (Jupiter engine) and TestNG tests so you can watch both engines report in a single `mvn test`. In a real project you'd pick one framework; the mix exists here only to keep every interview answer in one runnable place.

## How to practice with it

1. Pick a question, read its test class once, then delete the method bodies and rewrite them from memory until `mvn test` is green.
2. Say each annotation's purpose out loud while typing; interviewers grade the narration as much as the code.
3. Break a test on purpose (wrong expected value, missing `verify`) and read the failure output; explaining surefire reports is a frequent follow-up.
