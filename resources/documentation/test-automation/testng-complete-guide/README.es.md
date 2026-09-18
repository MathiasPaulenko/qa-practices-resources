# Guía Completa de TestNG — Companion

Recurso companion de [Guía Completa de TestNG: Paralelismo y Anotaciones](https://qapractices.com/es/documentation/testng-complete-guide).

Proyecto Maven ejecutable con los ejemplos de la guía: `CalculatorTest` con `@BeforeClass`/`@AfterClass` y `testName`, `LoginTest` con un `@DataProvider`, y un `testng.xml` con filtrado de grupos y ejecución paralela.

## Contenido

- `src/main/java/com/qapractices/Calculator.java` — clase bajo test (add, subtract, divide)
- `src/main/java/com/qapractices/AuthService.java` — servicio mínimo para el test de login con data provider
- `src/test/java/com/qapractices/CalculatorTest.java` — test de TestNG 7.12 con grupos y `testName`
- `src/test/java/com/qapractices/LoginTest.java` — test de login parametrizado con `@DataProvider`
- `src/test/resources/testng.xml` — config de suite con `parallel="methods"`, `thread-count="4"` y filtrado de grupos
- `pom.xml` — TestNG 7.12.0 + Surefire 3.2.5 conectado al archivo de suite

## Requisitos

- Java 17+
- Maven 3.9+

## Uso

```bash
mvn test                      # corre la suite completa (smoke + regression)
mvn test -Dgroups="smoke"     # corre solo el grupo smoke
mvn test -DexcludedGroups="regression"  # corre todo menos regression
```

Consulta la guía para el ciclo de vida de anotaciones, listeners, soft assertions y configuración de CI/CD.
