# Companion de Entrevista de Testing Java

Versiones ejecutables de las respuestas de la guía de QAPractices [Entrevista de Testing Java: Spring y JUnit](https://qapractices.com/es/documentation/java-testing-interview-questions/) ([English version](https://qapractices.com/documentation/java-testing-interview-questions/)).

## Qué contiene

| Archivo | Pregunta de entrevista que cubre |
|---|---|
| `examples/LifecycleAndAssertionsTest.java` | Q4 orden del ciclo de vida, Q5 `@DisplayName`, Q6 aserciones incluido `assertAll`, Q7 assumptions, Q17 `assertThrows` |
| `examples/ParameterizedExamplesTest.java` | Q8 `@ParameterizedTest` con `@ValueSource`, `@CsvSource`, `@MethodSource` |
| `examples/MockitoExamplesTest.java` | Q10 flujo `when`/`verify`, Q11 mock vs spy lado a lado, Q12 argument matchers incluidos `eq()` y `argThat()` |
| `examples/TestNgDataProviderTest.java` | Q9 `@DataProvider` de TestNG corriendo junto a JUnit 5 |
| `examples/pom.xml` | Configuración de Surefire 3.5.6 con includes/excludes; JUnit 5.12.2, Mockito 5.14.2, TestNG 7.10.2 |

## Cómo ejecutarlo

Necesitas JDK 17+ y Maven 3.9+.

```bash
cd examples
mvn test
```

La suite mezcla tests de JUnit 5 (motor Jupiter) y de TestNG para que veas ambos motores reportando en un solo `mvn test`. En un proyecto real elegirías un framework; la mezcla existe aquí solo para mantener todas las respuestas de la entrevista en un mismo lugar ejecutable.

## Cómo practicar con él

1. Elige una pregunta, lee su clase de test una vez, borra los cuerpos de los métodos y reescríbelos de memoria hasta que `mvn test` pase en verde.
2. Di en voz alta para qué sirve cada anotación mientras escribes; los entrevistadores evalúan la narración tanto como el código.
3. Rompe un test a propósito (valor esperado incorrecto, `verify` ausente) y lee la salida del fallo; explicar los informes de Surefire es una repregunta frecuente.
