# API Integration Tests — Companion

Companion ejecutable de [Cómo Escribir API Integration Tests](https://qapractices.com/es/documentation/how-to-write-api-integration-tests/) ([English version](https://qapractices.com/documentation/how-to-write-api-integration-tests/)).

## Qué incluye

- `js/` — una app mínima de Express 5 con almacenes en memoria, más una suite de Jest 30 + supertest 7 que cubre la cadena CRUD, la autenticación con token, los datos por test, las verificaciones de contrato, el encadenamiento de requests y los caminos de error de la guía.
- `python/` — una app de FastAPI más una suite de pytest 8 con el mismo flujo CRUD a través de `TestClient` y un fixture con `yield` para setup/teardown.
- `ci/` — un workflow de GitHub Actions con un servicio de Postgres 16 y health checks de `pg_isready`, igual que la sección de CI de la guía.

## Correr la suite de JavaScript

Requiere Node 20+.

```bash
cd js
npm install
npm test
```

La autenticación en memoria acepta cualquier contraseña no vacía para los usuarios de prueba (`test.user@test.dev`, `buyer@test.dev`, `admin@test.dev`), así que `TEST_USER_PASSWORD` y `TEST_ADMIN_PASSWORD` pueden tener cualquier valor o quedar vacías.

## Correr la suite de Python

Requiere Python 3.10+.

```bash
cd python
pip install -r requirements.txt
pytest
```

## Notas

Las apps guardan todo el estado en memoria: reiniciá el proceso y los datos vuelven a cero. Es a propósito — cada corrida de tests arranca con un almacén limpio, la misma garantía que la guía pide de una base de datos dedicada a pruebas.
