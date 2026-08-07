# Ejemplo de catálogo de libros con Behave BDD

Ejemplo completo y ejecutable de Behave para la guía [Behave BDD Project Setup Guide](https://qapractices.com/es/documentation/behave-bdd-project-setup-guide/).

Este proyecto muestra el mismo catálogo bajo tres capas de prueba distintas:

1. **Catálogo en memoria** — BDD de estilo unitario en Python directo.
2. **Catálogo vía API HTTP** — un pequeño `http.server` y un cliente `requests`.
3. **Catálogo con SQLite** — BDD respaldado por base de datos con rollback por savepoint.

## Ejecutar

```bash
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate en Windows
pip install -r requirements-dev.txt
```

### Ejecutar todas las features

```bash
behave
```

### Ejecutar solo una capa

```bash
# Catálogo en memoria
behave --tags='~api' --tags='~db'

# API HTTP
behave --tags=api

# SQLite
behave --tags=db
```

### Reportes para CI

```bash
mkdir -p reports
behave --junit --junit-directory=reports/junit --format=json --outfile=reports/behave-report.json
```

## Estructura del proyecto

```text
book-catalog/
├── catalog_service.py           # catálogo en memoria
├── catalog_db.py                # catálogo con SQLite
├── book_server.py               # servidor HTTP para la API
├── api_client.py                # wrapper de requests
├── behave.ini                   # configuración y userdata
├── requirements-dev.txt
├── pyproject.toml
└── features/
    ├── environment.py           # hooks unificados para las tres capas
    ├── book_catalog.feature     # escenarios en memoria
    ├── book_api.feature         # escenarios de API
    ├── book_catalog_db.feature  # escenarios de SQLite
    └── steps/
        ├── catalog_steps.py     # pasos para memoria y SQLite
        └── api_steps.py         # pasos para la API
```

## Tags

- `@smoke` — escenarios rápidos y representativos.
- `@regression` — cobertura extendida.
- `@api` — escenarios de API HTTP.
- `@db` — escenarios de SQLite.
- `@integration` — cambia `context.base_url` a `REAL_API_URL` desde `behave.ini`.
