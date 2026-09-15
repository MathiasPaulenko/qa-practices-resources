# Unit Testing Frameworks Comparison — Companion

Companion resource for [Unit Testing Frameworks Comparison](https://qapractices.com/documentation/unit-testing-frameworks-comparison).

## Contents

- `src/math.js` — Module under test (ESM)
- `src/math.test.js` — Jest 30.5 test with `jest.mock` for module mocking
- `src/math.test.ts` — Vitest 2.x test with `vi.mock` for module mocking
- `src/math.test.mocha.js` — Mocha + Chai + Sinon test (CJS)

## Requirements

- Node.js 20+
- Jest 30.5+ (for `.test.js`)
- Vitest 2.x (for `.test.ts`)
- Mocha 10.x + Chai 5.x + Sinon 18.x (for `.test.mocha.js`)

## Usage

Each file is a standalone example of the same test in a different framework. Copy the one matching your stack.

```bash
# Jest
npx jest src/math.test.js

# Vitest
npx vitest run src/math.test.ts

# Mocha
npx mocha src/math.test.mocha.js
```

See the comparison guide for the trade-offs between frameworks.
