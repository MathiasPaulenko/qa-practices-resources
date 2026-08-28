# Companion de Preguntas de Entrevista de API Testing Nexus Payments

Companion ejecutable para la guía de QAPractices [50 Preguntas de Entrevista de API Testing](https://qapractices.com/es/documentation/api-testing-interview-questions/).

## Qué incluye

Este companion replica el escenario de checkout `v3.2.5` de Nexus Payments de la guía de entrevista. Incluye:

- **`nexus-api-tests/`** — Proyecto Java 17 + REST Assured 5.4.0 + Maven 3.9 con:
  - `CheckoutTest.java` — camino feliz, cargo duplicado (409), idempotencia, rate-limit
  - `AuthTest.java` — validación JWT, token caducado, BOLA
  - `ContractTest.java` — validación JSON Schema para checkout y user
  - `RetryAnalyzer.java` — retroceso exponencial para endpoints con rate limit
  - `checkout-schema.json` / `user-schema.json` — contratos JSON Schema
  - `test-config.properties` — configuración de entorno
- **`postman/`** — Colección Postman v11 + entorno:
  - `nexus-checkout-smoke.json` — colección de smoke (debe terminar < 180s)
  - `nexus-qa-env.json` — variables de entorno QA
- **`.github/workflows/api-smoke.yml`** — Workflow de GitHub Actions que ejecuta smoke de Newman en cada PR

## Versiones del stack

| Herramienta | Versión |
| --- | --- |
| Java | 17 |
| REST Assured | 5.4.0 |
| Maven | 3.9 |
| Postman | v11.0.11 |
| Newman | 6.1.2 |
| JUnit | 5.10.2 |
| GitHub Actions | latest |

## Ejecutar las pruebas Java

```bash
cd nexus-api-tests
mvn clean test -Denv=qa
```

## Ejecutar el smoke de Postman

```bash
cd postman
newman run nexus-checkout-smoke.json -e nexus-qa-env.json --reporters cli,junit --reporter-junit-export results.xml
```

## El incidente 409

El test `CheckoutTest.duplicateChargeReturns409()` reproduce el incidente de la guía: `POST /v2/checkout` con el mismo `Stripe-Idempotency-Key` dos veces debería resultar en un cargo, no dos. El test afirma `409 Conflict` en la segunda llamada.

## Licencia

MIT — ver el repo principal para detalles.
