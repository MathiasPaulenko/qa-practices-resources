# Casos de Prueba de Búsqueda y Filtros — Companion Playwright

Código companion de [Casos de Prueba de Búsqueda y Filtros: Validación y UX](https://qapractices.com/es/test-cases/search-filter-test-cases/) en QAPractices.

## Qué hay dentro

| Archivo | Qué muestra |
|---------|-------------|
| `search-demo.html` | Página demo autocontenida: catálogo de 7 productos, input de búsqueda con debounce de 300ms, lógica OR-dentro-de-faceta / AND-entre-facetas, estado en URL, estado vacío, clear-all. Sin servidor — funciona con `file://`. |
| `tests/search-filter.spec.ts` | 8 specs de Playwright 1.48 cubriendo TC-01, TC-07, TC-08, TC-09, TC-11, TC-13, TC-15, TC-16. |
| `package.json` | `@playwright/test` pineado en 1.48.2. |

## Ejecutarlo

```bash
npm install
npx playwright install chromium   # navegadores, una sola vez
npm test
```

Todos los specs corren contra `search-demo.html` local — sin backend, sin red. El spec de debounce (TC-11) cuenta llamadas con el contador visible `#call-count`; el spec de estado en URL (TC-15) reabre la URL en una página nueva y compara los conjuntos de resultados.

## Recurso relacionado

- [Casos de Prueba de Búsqueda y Filtros: Validación y UX](https://qapractices.com/es/test-cases/search-filter-test-cases/) — la suite completa de 16 casos más la tabla de edge/boundary que este código automatiza.
