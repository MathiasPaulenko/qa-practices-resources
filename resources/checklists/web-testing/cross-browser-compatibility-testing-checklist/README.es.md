# Checklist de Matriz de Compatibilidad Cross-Browser — Companion

Archivos companion del recurso [Checklist de Matriz de Compatibilidad Cross-Browser](https://qapractices.com/es/checklists/cross-browser-compatibility-testing-checklist).

Las matrices vienen como CSV importables para pegarlas en una planilla, una herramienta de gestión de tests o un ticket de seguimiento sin reescribir nada.

## Archivos

| Archivo | Contenido |
|---|---|
| `browser-matrix.csv` | Filas de navegadores objetivo: motor, navegador, versión, SO/dispositivo, escala, prioridad, evidencia |
| `viewport-matrix.csv` | Filas de viewports: nombre, dimensiones, DPR, enfoque de prueba |
| `checklist-items.csv` | Los 29 ítems del checklist en 5 áreas (Paridad de Entorno, CSS y Renderizado, JavaScript y APIs, Formularios e Input, Edge y Negativos) con riesgo por ítem |

## Uso

- Importa `browser-matrix.csv` y `viewport-matrix.csv` en tu plan de pruebas y descarta las filas por debajo de tu cuota de analytics.
- Importa `checklist-items.csv` como tareas (Jira, TestRail o una planilla) y ordena por `risk` — corre `High` primero.
- Regenera las filas de navegadores desde tu propio analytics: mantén como P1 los motores que cubran ≥ 5% del tráfico.

Recurso en el sitio: [qapractices.com/es/checklists/cross-browser-compatibility-testing-checklist](https://qapractices.com/es/checklists/cross-browser-compatibility-testing-checklist)
