# Jest vs Vitest — Companion

Recurso complementario de [Jest vs Vitest: comparativa de frameworks de testing](https://qapractices.com/es/documentation/jest-vs-vitest).

## Contenido

- `side-by-side/package.json` — ambos runners instalados, con npm scripts separados para cada uno
- `side-by-side/jest.config.js` — config mínima de Jest 30.5 con un alias `moduleNameMapper`
- `side-by-side/babel.config.js` — `@babel/preset-env` para que Jest pueda parsear los mismos archivos ESM que Vitest corre de forma nativa
- `side-by-side/vite.config.ts` — config de Vitest 5.0 que comparte el mismo alias `@/` vía `resolve.alias`
- `side-by-side/src/validators.js` — validadores de email y contraseña (JS plano)
- `side-by-side/src/cart.js` — totales de carrito y lógica de descuentos
- `side-by-side/__tests__/validators.test.js` — idéntico bajo ambos runners vía globals
- `side-by-side/__tests__/cart.test.js` — ejercita el alias `@/` para demostrar la paridad de configuración

## Requisitos

- Node 22.12+ (requisito de Vitest 5)
- npm

## Uso

```bash
cd side-by-side
npm install

npm run test:jest      # Jest 30.5
npm run test:vitest    # Vitest 5.0
npm run test:watch     # Watch mode de Vitest sobre HMR

npm run coverage:jest    # Instrumentación Istanbul
npm run coverage:vitest  # Instrumentación v8 — los números difieren levemente por provider
```

El punto de la demo: los mismos archivos de `__tests__/` pasan bajo ambos runners sin modificación — `describe`, `it`, `test` y `expect` son idénticos. Las diferencias viven en la configuración (`moduleNameMapper` vs `resolve.alias`) y en las APIs solo-Jest (`jest.mock`, `jest.useFakeTimers`) que se mapean a `vi.*` del lado de Vitest.

Mirá la guía para el checklist completo de migración, el árbol de decisión y los números de producción de una migración real de Jest a Vitest.
