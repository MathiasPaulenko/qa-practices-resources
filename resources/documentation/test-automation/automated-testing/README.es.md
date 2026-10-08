# Pruebas Automatizadas — Ejemplos del Playbook de Decisión de LedgerFlow

> Recurso complementario de [Pruebas Automatizadas: La Decisión Real de un Equipo QA](https://qapractices.com/es/documentation/automated-testing) en QAPractices.com.

Versiones ejecutables de los snippets de la guía: un test unitario de Jest 29 para el cálculo de impuestos de LedgerFlow, un test de contrato de API con Playwright 1.44, un flujo E2E de factura con Playwright, y el workflow de GitHub Actions de tres jobs (unit / integration / e2e).

## Requisitos

- Node.js 20
- Jest 29
- Playwright 1.44
- Postgres 15 y Redis 7 (para el job de integración en CI, vía Docker Compose o servicios de GitHub Actions)

## Setup

```bash
# Instalar dependencias
npm ci

# Correr los tests unitarios
npm run test:unit

# Instalar navegadores de Playwright y correr suites de API / E2E
# (requieren una app corriendo; define BASE_URL para apuntar a ella)
npx playwright install --with-deps chromium
npm run test:api
npm run test:e2e
```

El test unitario corre directamente contra `src/tax/calculateTax.js`. Los specs de API y E2E apuntan a la app ficticia LedgerFlow descrita en la guía: sirven como plantillas para adaptar a tus propias rutas y atributos `data-testid`.

## Estructura del Proyecto

```text
src/
  tax/calculateTax.js        # unidad bajo prueba
tests/
  unit/calculateTax.test.js  # test unitario Jest 29
  api/invoices.spec.js       # test de API Playwright 1.44
  e2e/send-invoice.spec.js   # test E2E Playwright 1.44
.github/workflows/test.yml   # pipeline unit / integration / e2e
```

## Licencia

MIT — ver el archivo LICENSE en la raíz del repositorio.
