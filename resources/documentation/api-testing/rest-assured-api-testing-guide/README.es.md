# Companion de la Guía de Testing con REST Assured

Recurso companion de la [Guía de Testing con REST Assured](https://qapractices.com/es/documentation/rest-assured-api-testing-guide). Incluye un proyecto Maven con REST Assured 5.4.0, JUnit 5.10.2, Hamcrest 2.2, validación de JSON Schema, y un workflow de CI con GitHub Actions.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `pom.xml` | Configuración Maven con REST Assured 5.4.0, JUnit 5.10.2, Hamcrest 2.2 |
| `src/test/java/com/qapractices/UserCrudTest.java` | Clase de test CRUD con ejecución ordenada |
| `src/test/java/com/qapractices/AuthTest.java` | Tests de autenticación (Basic, Bearer, OAuth2, API Key) |
| `src/test/resources/schemas/user-schema.json` | JSON Schema para validación de respuesta de usuario |
| `.github/workflows/api-tests.yml` | Workflow de CI que corre `mvn clean test` en push/PR |

## Inicio Rápido

```bash
mvn clean test
```

## Requisitos

- Java 17+
- Maven 3.9+
- Acceso a internet (los tests corren contra https://reqres.in)
