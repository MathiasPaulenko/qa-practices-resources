# Pruebas de Paginación de API — Companion

Recurso complementario de [Pruebas de Paginación de API: 14 Escenarios](https://qapractices.com/es/test-cases/api-pagination-testing-test-cases).

## Contenido

- `mock_server.py` — API paginada solo-stdlib (offset, cursor y keyset) sobre 247 productos en memoria, más `POST /products` para escenarios de inserción concurrente
- `tests/conftest.py` — levanta el mock server en un puerto efímero por sesión de tests
- `tests/test_boundaries.py` — límites de tamaño de página, última página, dataset vacío, cursor inválido (tabla edge + TC-01..07, TC-12)
- `tests/test_cursor_pagination.py` — consistencia cursor/keyset, inmunidad a inserts concurrentes, preservación de filtros (TC-09, TC-11)
- `tests/test_offset_pagination.py` — recorrido del dataset completo, desempate de ordenamiento, offset profundo, `total_count` acotado, gap documentado de offset (TC-08, TC-10, TC-13, TC-14)
- `requirements.txt` — pytest 8.3 + requests

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
pytest tests/ -v
```

El mock server también corre standalone para checks manuales:

```bash
python mock_server.py 8571
curl "http://127.0.0.1:8571/products?limit=10"
```

El punto de la demo: los bugs de paginación solo aparecen bajo condiciones de borde y concurrencia que un test de camino feliz nunca toca — offsets profundos, últimas páginas parciales, inserts a mitad de paginación, columnas de ordenamiento no únicas. El mock codifica esas condiciones (timestamps compartidos, 247 ítems para que `limit=10` produzca una última página parcial) y hace reproducible localmente cada escenario de la guía.

Mirá la guía para las tablas completas de casos, los trade-offs offset-vs-cursor y la historia de campo detrás del TC-10.
