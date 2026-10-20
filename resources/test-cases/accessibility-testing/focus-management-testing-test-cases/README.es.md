# Casos de Prueba de Gestión del Foco — Laboratorio Companion

Companion del recurso [Casos de Prueba de Gestión del Foco](https://qapractices.com/es/test-cases/focus-management-testing-test-cases/) en QAPractices.com.

`focus_model.py` es un pequeño modelo en Python (solo stdlib) del contrato de foco por teclado: orden de tabulación del DOM, secuestro por `tabindex` positivo, enlaces de salto, trampa en modal y retorno al disparador, destinos tras eliminación de nodos y foco por script con `tabindex="-1"`. Codifica las *reglas* para ejercitar las aserciones sin navegador — las comprobaciones reales usan `keyboard` de Playwright + `document.activeElement`, como muestra el recurso.

## Qué cubre el modelo

- **Orden de tabulación (TC-001/TC-010):** hacia adelante y `Shift+Tab` inverso siguen el orden del DOM; los nodos ocultos se saltan.
- **Enlaces de salto (TC-004):** el primer `Tab` alcanza el enlace; activarlo aterriza en el landmark principal.
- **Trampa en modal y retorno (TC-005):** el foco entra dentro, cicla en ambas direcciones y `Escape` restaura el disparador — nunca `body`.
- **tabindex positivo (TC-007):** `tabindex > 0` se detecta y se muestra cómo secuestra el orden de la página.
- **Eliminación dinámica (TC-012):** un nodo enfocado eliminado aterriza en un destino definido, no en `document.body`.
- **`tabindex="-1"` (TC-014):** ausente del orden de tabulación, enfocable por script.

## Ejecutar

```bash
pip install -r requirements.txt
pytest -v
```

Esperado: `23 passed` en menos de un segundo — solo stdlib, sin navegador.

## Archivos

- `focus_model.py` — `Page`, `Focusable`, `Modal`, `FocusModelError`.
- `tests/test_focus_model.py` — 23 tests agrupados por los ids TC del recurso.
- `requirements.txt`, `pytest.ini` — pytest 8.3.4 fijado.
