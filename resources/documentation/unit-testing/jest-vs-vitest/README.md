# Jest vs Vitest — Companion

Companion resource for [Jest vs Vitest: JavaScript Testing Comparison](https://qapractices.com/documentation/jest-vs-vitest).

## Contents

- `side-by-side/package.json` — both runners installed, separate npm scripts for each
- `side-by-side/jest.config.js` — minimal Jest 30.5 config with a `moduleNameMapper` alias
- `side-by-side/babel.config.js` — `@babel/preset-env` so Jest can parse the same ESM test files Vitest runs natively
- `side-by-side/vite.config.ts` — Vitest 5.0 config sharing the same `@/` alias via `resolve.alias`
- `side-by-side/src/validators.js` — email and password validators (plain JS)
- `side-by-side/src/cart.js` — cart totals and discount logic
- `side-by-side/__tests__/validators.test.js` — identical under both runners via globals
- `side-by-side/__tests__/cart.test.js` — exercises the `@/` alias to prove config parity

## Requirements

- Node 22.12+ (Vitest 5 requirement)
- npm

## Usage

```bash
cd side-by-side
npm install

npm run test:jest      # Jest 30.5
npm run test:vitest    # Vitest 5.0
npm run test:watch     # Vitest HMR-powered watch mode

npm run coverage:jest    # Istanbul instrumentation
npm run coverage:vitest  # v8 instrumentation — numbers differ slightly by provider
```

The point of the demo: the same `__tests__/` files pass under both runners without modification — `describe`, `it`, `test` and `expect` are identical. The differences live in configuration (`moduleNameMapper` vs `resolve.alias`) and in Jest-only APIs (`jest.mock`, `jest.useFakeTimers`) that map to `vi.*` on the Vitest side.

See the guide for the full migration checklist, the decision tree, and the production numbers from a real Jest → Vitest migration.
