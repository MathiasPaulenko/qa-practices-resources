# Casos de Prueba de Infinite Scroll — Lab Companion

Companion de [Casos de Prueba de Infinite Scroll: Ejemplo TaskFlow](https://qapractices.com/es/test-cases/infinite-scroll-pagination-test-cases/) en QAPractices.

Modelo de Python puro (stdlib) de un feed de infinite scroll: `PaginatedAPI`
sirve páginas por offset (`page=N`, `hasMore`, fallos inyectables) y
`ScrollFeed` hace de cliente — fetch al umbral, append con dedupe por id,
detección de fin de feed y retry idempotente.

## Estructura

```text
paginated_feed.py              — PaginatedAPI + ScrollFeed + make_tasks helper
tests/test_paginated_feed.py   — casos pytest mapeados a los TC-xxx del sitio
requirements.txt               — pytest 8.3.4
pytest.ini                     — testpaths/pythonpath
```

## Ejecutar

```bash
pip install -r requirements.txt
pytest -q
```

## Cobertura

Primera/parcial/última página, append de página 2 con dedupe por id, fin de
feed (sin request a `page=6`), errores a mitad de scroll preservando ítems
renderizados, retry idempotente, rechazo de página duplicada, feed vacío y los
límites (múltiplo exacto vs total+1).

El modelo es offline y determinista — sirve para prototipar la lógica de
dedupe/retry antes de cablear la implementación real con `IntersectionObserver`.
