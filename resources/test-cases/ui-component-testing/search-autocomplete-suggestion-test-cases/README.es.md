# Casos de Prueba de Autocompletado — Companion

Recurso complementario de [Casos de Prueba de Autocompletado: Debounce, Teclado, ARIA](https://qapractices.com/es/test-cases/search-autocomplete-suggestion-test-cases/).

## Contenido

- `autocomplete_engine.py` — modelo en Python stdlib de un cliente de autocompletado con debounce sobre un reloj virtual: puerta de longitud mínima, ventana de debounce de 300ms, caché con TTL, guardia última-query-gana contra respuestas desordenadas, dedup, tope de render, resaltado de substring, recientes y semántica de Escape/limpiar.
- `autocomplete.html` — fixture estático que implementa el combobox ARIA real (role/expanded/controls/activedescendant, listbox, options, status `aria-live`, navegación por teclado, resaltado con `<mark>`, recientes en localStorage) para verificación manual y con Playwright. Abrilo en cualquier navegador.
- `tests/conftest.py` — agrega el motor al `sys.path`.
- `tests/test_autocomplete_engine.py` — subconjunto ejecutable de los casos del artículo: colapso de debounce (TC-02), tecla en el límite de 300ms (edge), pegado como un evento (edge), puerta de longitud mínima (TC-14), hit de caché (TC-07) y vencimiento de TTL (TC-16), última-query-gana desordenada (TC-11), error de API + reintento (TC-12), estado de carga (TC-13), sin resultados (TC-08), dedup (TC-18), tope de render (edge), resaltado (TC-06), recientes con foco en vacío (TC-09), Escape conserva query (TC-05) y reseteo de limpiar (TC-26).

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Salida esperada: `16 passed`.

El fixture de navegador no necesita build: abrí `autocomplete.html` y escribí — el debounce, la caché, la guardia de respuestas stale y el contrato ARIA se ejercitan en vivo.

## Relacionado

- Artículo EN: https://qapractices.com/test-cases/search-autocomplete-suggestion-test-cases/
- Artículo ES: https://qapractices.com/es/test-cases/search-autocomplete-suggestion-test-cases/
