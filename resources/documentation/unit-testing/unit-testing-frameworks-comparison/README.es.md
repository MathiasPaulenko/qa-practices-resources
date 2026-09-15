# Unit Testing Frameworks Comparison — Companion (ES)

Recurso companion para [Comparativa de Frameworks de Unit Testing](https://qapractices.com/es/documentation/unit-testing-frameworks-comparison).

## Contenido

- `src/math.js` — Módulo bajo test (ESM)
- `src/math.test.js` — Test en Jest 30.5 con `jest.mock` para mockear módulos
- `src/math.test.ts` — Test en Vitest 2.x con `vi.mock` para mockear módulos
- `src/math.test.mocha.js` — Test en Mocha + Chai + Sinon (CJS)

## Requisitos

- Node.js 20+
- Jest 30.5+ (para `.test.js`)
- Vitest 2.x (para `.test.ts`)
- Mocha 10.x + Chai 5.x + Sinon 18.x (para `.test.mocha.js`)

## Uso

Cada archivo es un ejemplo standalone del mismo test en un framework diferente. Copia el que coincida con tu stack.

```bash
# Jest
npx jest src/math.test.js

# Vitest
npx vitest run src/math.test.ts

# Mocha
npx mocha src/math.test.mocha.js
```

Consulta la guía comparativa para los trade-offs entre frameworks.
