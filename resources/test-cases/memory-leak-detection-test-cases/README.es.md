# Casos de Prueba de Fugas de Memoria

> Companion imprimible y ejemplos ejecutables de [Casos de Prueba de Fugas de Memoria](https://qapractices.com/es/test-cases/memory-leak-detection-test-cases).

Este repositorio contiene una versión imprimible del conjunto de casos de prueba más scripts de ejemplo para adaptar a tu proyecto.

## Archivos

- `memory-leak-detection-test-cases.es.md` — Versión en Markdown, lista para pegar en una herramienta de test management.
- `memory-leak-detection-test-cases.json` — JSON estructurado con todos los casos, casos de borde y prioridades.
- `scripts/` — Scripts de ejemplo:
  - `node-heap-baseline.js` — Capturar una lectura baseline de `heapUsed`.
  - `node-heap-monitor.js` — Monitorear `process.memoryUsage()` en el tiempo.
  - `playwright-spa-memory.test.js` — Test de Playwright para DOM nodes detached.

## Cómo usar

1. Abrí `memory-leak-detection-test-cases.es.md` en tu herramienta de test management.
2. Ejecutá `node scripts/node-heap-baseline.js` para establecer un baseline en tu ambiente.
3. Ejecutá `node scripts/node-heap-monitor.js` mientras aplicás carga.
4. Usá `playwright-spa-memory.test.js` como punto de partida para tests de SPA.

## Requisitos

- Node.js 20+ (para `--heapsnapshot-near-heap-limit` y `process.memoryUsage()`)
- Playwright 1.48+ (para tests de SPA)
- Chrome / Chromium (para heap snapshots de DevTools)
