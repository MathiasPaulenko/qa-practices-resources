# Casos de Prueba de Integración

> Ejemplos ejecutables para [Casos de Prueba de Integración](https://qapractices.com/es/test-cases/integration-testing-test-cases).

Este companion contiene ejemplos ejecutables que cubren los escenarios de integración más comunes: escrituras de API a base de datos, llamadas entre servicios y un flujo de pedido end-to-end con aserciones de efectos laterales.

## Archivos

- `docker-compose.yml` — App más Postgres para corridas locales de integración.
- `scripts/test_api_db_integration.py` — pytest + requests: POST vía API, verificar la fila en la base de datos (TC-001).
- `scripts/test_order_flow.spec.ts` — test de Playwright: flujo de pedido asegurando el estado de inventario en ambos lados de la costura (TC-009).

## Cómo usar

1. `docker compose up -d` para levantar la app y la base de datos.
2. `pytest scripts/test_api_db_integration.py -v` para el check de API a base de datos.
3. `npx playwright test scripts/test_order_flow.spec.ts` para el flujo de pedido E2E (requiere Playwright 1.48+ y una app corriendo en `BASE_URL`).

## Requisitos

- Docker + Docker Compose
- Python 3.10+ con `pytest` y `requests` 2.x
- Node.js 18+ con `@playwright/test` 1.48+
