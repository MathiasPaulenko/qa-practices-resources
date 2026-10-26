# Casos de Prueba de Manejo de Errores en API — Companion

Companion ejecutable de [Casos de Prueba de Manejo de Errores en API: 4xx, 5xx y Contratos](https://qapractices.com/es/test-cases/api-error-handling-test-cases/).

## Contenido

| Archivo | Herramienta | Qué cubre |
|---|---|---|
| `test_error_handling.py` | pytest 8.3 + requests 2.32 | TC-001, TC-002, TC-006, TC-009, TC-017 — challenge de auth, `Allow` de método, `Retry-After` de rate limit, forma problem-details |
| `problem-details-schema.json` | jsonschema 4.x | JSON Schema del contrato RFC 9457 `application/problem+json` usado por TC-017 |

## Setup

```bash
pip install pytest requests jsonschema
export API_BASE_URL="https://api.staging.example.com/api/v1"
```

`api.staging.example.com` es un placeholder — apuntalo a tu propio entorno. Nunca corras el test de rate limit contra un endpoint de producción sin coordinarlo antes.

## Ejecutar

```bash
pytest test_error_handling.py -v
```

Definí `API_BASE_URL` antes de correr; los tests se saltean si no está seteada.
