# Testing de Sort y Filtro de Tablas de Datos — Companion

Recurso complementario de [Casos de Prueba de Tabla de Datos: Ordenar, Filtrar, Buscar](https://qapractices.com/es/test-cases/data-table-sort-filter-test-cases/).

## Contenido

- `mock_server.py` — mock solo stdlib de la API ficticia `api.datagridpro.io` usada en el artículo. Implementa `GET /v1/orders` con los parámetros `sort`, `direction`, `page`, `pageSize`, `status`, `from`, `to` y `search`, más autenticación Bearer.
- `tests/conftest.py` — levanta el mock en un puerto efímero por test.
- `tests/test_orders_api.py` — subconjunto ejecutable de los casos del artículo: sort numérico vs lexicográfico (TC003), búsqueda y filtros combinados AND (TC005/TC008), matemática de paginación y recálculo de páginas tras filtrar (TC009/TC016), payload de estado vacío, caracteres especiales, campo de sort inválido y rechazo sin auth.

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
cd resources/test-cases/ui-component-testing/data-table-sort-filter-test-cases
pytest tests/ -v
```

Para ejecutar el mock de forma independiente:

```bash
python mock_server.py

curl "http://127.0.0.1:8080/v1/orders?sort=amount&direction=asc&pageSize=5" \
  -H "Authorization: Bearer cualquier-token"
```

## Qué cubre

- Ordenamiento por `amount`, `orderDate`, `customerName` y `status`, ascendente y descendente, con orden numérico real (2.50 antes que 10.00).
- Filtros: `status`, rango de fechas (`from`/`to`, inclusivo) y `search` global sobre id, nombre de cliente y status, combinados con lógica AND.
- Metadata de paginación (`page`, `pageSize`, `totalItems`, `totalPages`) y cómo `totalPages` se recalcula cuando un filtro achica el conjunto.
- Casos de error: sin Bearer token → `401`, campo de sort desconocido → `400`, caracteres especiales en búsqueda → `200` seguro.
