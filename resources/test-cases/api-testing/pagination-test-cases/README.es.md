# Casos de Prueba de Paginación: suite pytest ejecutable

Complemento de la guía de QAPractices [Casos de Prueba de Paginación: Offset, Cursor e Infinite Scroll](https://qapractices.com/es/test-cases/pagination-test-cases/).

Una mini-app Flask que sirve paginación offset (`?page&limit`) y cursor (`?limit&cursor`) sobre un dataset sembrado, más una suite pytest 8.3 que implementa los casos de API TC-01–TC-05 y TC-08–TC-10. TC-06/TC-07 (infinite scroll) son casos de UI — el snippet de Playwright de la guía cubre esos.

## Estructura del proyecto

```text
├── app.py            # App Flask: dataset sembrado, estrategias offset + cursor
├── test_pagination.py
└── requirements.txt
```

## Mapeo de conceptos

| Caso de prueba | Qué prueba | Función |
|---|---|---|
| TC-01/02/08 | Metadata offset: `total`, `totalPages`, `hasNextPage` | `test_tc01_*`, `test_tc02_*`, `test_tc08_*` |
| Filas de borde | `page=0`, `limit>max`, negativo, más-allá-de-la-última | `test_page_*` |
| TC-03/04 | Recorrido por cursor + cursor inválido 400 | `test_tc03_*`, `test_tc04_*` |
| TC-05 | Orden estable en el borde de página (desempate por id) | `test_tc05_*` |
| TC-10 | Desplazamiento offset vs estabilidad de cursor ante insert | `test_tc10_*` |

## Requisitos

- Python 3.10+, `pip install -r requirements.txt` (Flask 3.x, pytest 8.3).

## Uso

```bash
pip install -r requirements.txt
pytest -v
```

Sin servidor — los tests usan el test client de Flask. Para probar la API a mano:

```bash
python app.py   # sirve en :5000
curl "http://localhost:5000/items?page=1&limit=10"
```
