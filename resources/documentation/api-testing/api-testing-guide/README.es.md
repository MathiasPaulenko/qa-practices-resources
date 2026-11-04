# Companion de la Guía de Pruebas de API

Recurso companion de la [Guía de Pruebas de API: Técnicas Prácticas](https://qapractices.com/es/documentation/api-testing-guide). Contiene un proyecto Maven con REST Assured 5.4.0, JUnit 5.10.2, Hamcrest 2.2 y validación de esquema JSON contra un esquema derivado de OpenAPI.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `pom.xml` | Configuración Maven con REST Assured 5.4.0, json-schema-validator 5.4.0, JUnit 5.10.2, Hamcrest 2.2 |
| `src/test/java/com/qapractices/UsersApiContractTest.java` | Prueba de contrato: validación de esquema más checks negativos (401, 404) |
| `src/test/resources/schemas/users.json` | JSON Schema para la respuesta de lista de `/api/v1/users` |

## Inicio Rápido

```bash
export API_BASE_URL=https://staging.qapractices.com
export STAGING_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
mvn clean test
```

## Requisitos

- Java 17+
- Maven 3.9+
- Una URL base de API alcanzable (por defecto `https://staging.qapractices.com`, se sobreescribe con `API_BASE_URL`)
- Un token bearer válido para endpoints protegidos (`STAGING_TOKEN`)

## Notas

- `users.json` se deriva de la especificación OpenAPI 3.0 del endpoint de usuarios. Regenéralo cuando cambie el contrato.
- Las pruebas negativas afirman el contrato de error (`401` para tokens inválidos, `404` para recursos inexistentes). Ajusta los códigos esperados si tu API documenta un comportamiento distinto.
- Para desarrollo local sin backend real, apunta `API_BASE_URL` a una instancia de WireMock 3.x o MockServer que sirva el mismo contrato.
