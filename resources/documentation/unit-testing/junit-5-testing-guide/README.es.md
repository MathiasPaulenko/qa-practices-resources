# Guía de JUnit 5 — Companion

Companion para [Guía de JUnit 5 para Desarrolladores Java](https://qapractices.com/es/documentation/junit-5-testing-guide).

## Contenido

- `src/Calculator.java` — Clase de dominio usada en los ejemplos de test
- `src/CalculatorTest.java` — Test básico con `@BeforeEach`, `@DisplayName`, assertions
- `src/ParameterizedTestExample.java` — `@ParameterizedTest` con `@ValueSource`, `@MethodSource`, `@CsvSource`
- `src/UserServiceTest.java` — Clases `@Nested` para agrupar por contexto
- `src/TimingExtension.java` — Extensión custom `@ExtendWith` para timing de tests

## Requisitos

- Java 17+
- JUnit 5.11+ (Jupiter)

## Uso

Son snippets de referencia, no un proyecto Maven ejecutable. Copia las clases de test a tu proyecto y agrega la dependencia de JUnit 5:

```xml
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.11.0</version>
    <scope>test</scope>
</dependency>
```

Consulta la guía para el setup completo con Maven Surefire.
