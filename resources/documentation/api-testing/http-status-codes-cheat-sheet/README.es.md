# Cheat Sheet de Códigos de Estado HTTP — Companion

Archivos ejecutables para la guía [Códigos de Estado HTTP: Cheat Sheet para Testers](https://qapractices.com/es/documentation/http-status-codes-cheat-sheet).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `data/status-code-matrix.csv` | Matriz de códigos positiva/negativa lista para importar (12 escenarios) |
| `tests/test_status_codes.py` | Tests de contrato con pytest + requests 2.32 para 200/201/204/401/403/404/405/422/429 |
| `postman/status-code-assertions.js` | Snippets para la pestaña Tests de Postman v11 / Newman 6.x |
| `java/StatusCodeMatrixTest.java` | Ejemplos con REST Assured 5.5 + JUnit 5 para la misma matriz |

## Inicio Rápido

```bash
# Tests de contrato en Python (Python 3.10+, pytest 8.x, requests 2.32)
pip install requests pytest
BASE_URL=https://staging.qapractices.com pytest tests/test_status_codes.py -v

# Snippets de Postman: pegar en la pestaña Tests de cada request,
# o ejecutar la colección con Newman 6.x
newman run your-collection.json --environment staging.json

# REST Assured (proyecto Maven/Gradle con io.rest-assured:rest-assured:5.5.x)
mvn test -Dtest=StatusCodeMatrixTest -DBASE_URL=https://staging.qapractices.com
```

La matriz CSV puede importarse en una herramienta de gestión de tests
o usarse como entrada data-driven para el archivo pytest.

## Notas

- Apuntá `BASE_URL` a un entorno de staging o a un mock server
  (WireMock, Mockoon, Prism): los tests asumen una API CRUD `/users`.
- `test_rate_limit_returns_429_with_retry_after` depende del entorno;
  ajustá la cantidad de requests a tu límite real.
