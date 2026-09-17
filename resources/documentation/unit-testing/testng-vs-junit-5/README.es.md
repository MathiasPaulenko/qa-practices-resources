# TestNG vs JUnit 5 — Companion

Companion para [TestNG vs JUnit 5: Cuál Elegir](https://qapractices.com/es/documentation/testng-vs-junit-5).

## Contenido

- `src/LoginTests.java` — TestNG 7.10: test de login con `@DataProvider` + `@Test(dataProvider)`
- `src/DataProviderExample.java` — `@DataProvider` de TestNG vs `@ParameterizedTest`/`@CsvSource` de JUnit 5 lado a lado
- `src/DependencyTests.java` — `dependsOnMethods` de TestNG para flujos encadenados (login → dashboard → logout)
- `src/testng.xml` — Config de suite TestNG con `parallel="methods"` y filtrado de grupos
- `src/junit-platform.properties` — Configuración de ejecución paralela de JUnit 5.11

## Requisitos

- Java 17+
- TestNG 7.10+
- JUnit 5.11+ (Jupiter)

## Uso

Snippets de referencia, no un proyecto Maven ejecutable. Copia a tu proyecto y agrega las dependencias:

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

Ambos frameworks pueden coexistir en el mismo módulo Maven — Surefire levanta cada provider automáticamente. Consulta la guía para el ejemplo de migración completo y los criterios de decisión.
