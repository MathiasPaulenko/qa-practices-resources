# Casos de Prueba de Slider Range Input — Companion

Recurso complementario de [Casos de Prueba de Slider: Drag, Teclado y Steps](https://qapractices.com/es/test-cases/slider-range-input-test-cases/).

## Contenido

- `mock_server.py` — mock solo-stdlib de la API ficticia `api.rangesliderpro.io` usada en el artículo. Implementa `GET /v1/products` (`minPrice`, `maxPrice`, `step`, `page`, `pageSize`, auth Bearer), `POST /v1/sliders/validate` (min/max/step/value → validez + `nearestValidValue`), `POST /v1/sliders/validate-range` (handles cruzados + enforcement de `minGap`) y `POST /v1/users/{id}/preferences` (auth Bearer).
- `slider.html` — fixture estático para verificación manual de los casos de UI: un `<input type="range">` nativo (min=0, max=1000, step=5) con tooltip en vivo, input numérico linkeado bidireccional y una emulación dual-handle que enforces `minGap=10`. Abrilo en cualquier navegador.
- `tests/conftest.py` — levanta el mock en un puerto efímero por test.
- `tests/test_sliders_api.py` — subconjunto ejecutable de los casos del artículo: filtrado por rango de precio, paginación, rechazo de auth, validación de múltiplo de step, clampeo de min/max, rechazo no numérico, borde del min gap (`490/500` permitido, `495/500` rechazado) y persistencia de preferencias.

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
cd resources/test-cases/ui-component-testing/slider-range-input-test-cases
pytest tests/ -v
```

Corré el mock standalone para verificaciones manuales:

```bash
python mock_server.py

curl "http://127.0.0.1:8080/v1/products?minPrice=50&maxPrice=500&step=5&pageSize=5" \
  -H "Authorization: Bearer cualquier-token"
```

## Qué cubre

- `GET /v1/products` — filtrado por rango de precio + step, metadata de paginación y auth Bearer.
- `POST /v1/sliders/validate` — validación de múltiplo de step, clampeo min/max con `nearestValidValue`, rechazo no numérico.
- `POST /v1/sliders/validate-range` — rechazo de handles cruzados y el borde del `minGap` (exactamente en el gap pasa, dentro del gap falla).
- `POST /v1/users/{id}/preferences` — persistencia de preferencias con auth y validación de campos requeridos.
- `slider.html` — fixture manual para TC-001 (drag), TC-005 (snap), TC-010–TC-013 (input linkeado + input inválido) y TC-008 (min gap) sin una app real.
