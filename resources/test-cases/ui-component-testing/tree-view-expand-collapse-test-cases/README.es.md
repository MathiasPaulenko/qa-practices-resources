# Testing de Vista de Árbol Expandir/Colapsar — Companion

Recurso companion de [Casos de Prueba de Vista de Árbol: Expandir y Colapsar](https://qapractices.com/es/test-cases/tree-view-expand-collapse-test-cases/).

## Contenido

- `tree_model.py` — modelo ejecutable solo-stdlib de la lógica de una vista de árbol: expansión/colapso con snapshot y restauración del estado (persistencia en re-render), lazy loading con fetcher inyectable y estado de error reintentable, selección única, navegación por teclado (flechas, Home/End, type-ahead), cascade de checkboxes con estado indeterminate, drag-and-drop con rechazo de referencias circulares y filtro de búsqueda que conserva el contexto de los ancestros.
- `tests/test_tree_model.py` — suite pytest 8.3 que ejercita el modelo contra los casos de prueba TC001–TC024 del artículo.
- `fixtures/tree.json` — la jerarquía Documents/Work/Personal/Projects usada en el artículo.

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
cd resources/test-cases/ui-component-testing/tree-view-expand-collapse-test-cases
pytest tests/ -v
```

## Qué cubre

- Ciclo de vida de la expansión: expandir, colapsar, orden de visibilidad (TC001–TC005, TC011).
- Lazy loading: éxito, error 500 con estado colapsado reintentable, caché de cargados (TC012–TC013).
- Persistencia de estado: snapshot/restore de IDs expandidos tras reconstruir el árbol (TC014).
- Contrato de teclado: flechas, Home/End, type-ahead sin coincidencia (TC006–TC007, TC022–TC023).
- Cascade de checkboxes: checked → indeterminate al desmarcar parcial (TC024).
- Validación de drag-and-drop: mover entre padres, rechazar drops sobre sí mismo o descendientes (TC016–TC017).
- Filtro de búsqueda: nodos coincidentes más el camino de ancestros (TC015).
