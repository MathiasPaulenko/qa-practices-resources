# Casos de Prueba de Tooltips Hover/Focus — Companion

Recurso companion de [Casos de Prueba de Tooltips: Delay, Posición y Contenido](https://qapractices.com/es/test-cases/tooltip-hover-focus-test-cases/).

## Contenido

- `tooltip_engine.py` — modelo en stdlib del ciclo de vida del tooltip del artículo: `TooltipController` con reloj virtual (retardos de aparición/ocultación, supresión en tránsito, supresión por Escape, salidas instantáneas por scroll/desmontaje, paridad foco/blur), `resolve_position` (auto-flip con lado preferido + orden de fallback + clamp al viewport) y `check_aria_contract` (cableado de role/aria-describedby).
- `tooltip.html` — fixture estático que implementa el componente real para verificación manual y con Playwright: icono de ayuda, botones de barra solo con icono, Publicar deshabilitado con wrapper enfocable, etiqueta truncada en la barra lateral, disparadores en bordes superior/derecho con auto-flip, descarte con Escape y soporte de `prefers-reduced-motion`. Ábrelo en cualquier navegador.
- `tests/conftest.py` — añade el motor al `sys.path`.
- `tests/test_tooltip_engine.py` — subconjunto ejecutable de los casos del artículo: gating por retardo (TC-002), tránsito que nunca monta (fila 1 de bordes), el cruce del hueco cancela la ocultación (TC-013/TC-022), supresión por Escape (TC-007), paridad foco/blur (TC-006), salidas instantáneas (TC-018/fila 4 de bordes), contenido vacío (TC-016), persistencia (TC-026), flips top→bottom y right→left (TC-011/TC-012), fallback con clamp (TC-024) y el contrato ARIA (TC-021/fila 5 de bordes).

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
cd resources/test-cases/ui-component-testing/tooltip-hover-focus-test-cases
pytest tests/ -v
```

Comprobaciones manuales: abre `tooltip.html` en un navegador — pasa el cursor por el icono "ⓘ", haz Tab hasta él, pulsa Escape y haz scroll para ver las salidas instantáneas.

## Qué cubre

- `TooltipController` — el contrato de timing (500ms de aparición, 300ms de ocultación) y el modelo de eventos detrás de la tabla de bordes.
- `resolve_position` — el árbol de decisión de auto-flip detrás de TC-011, TC-012 y TC-024.
- `check_aria_contract` — el cableado `role="tooltip"` / `aria-describedby` detrás de TC-021.
- `tooltip.html` — fixture manual para el snippet Playwright de la sección Ejemplo de Automatización del artículo.
