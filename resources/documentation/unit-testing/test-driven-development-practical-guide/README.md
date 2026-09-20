# TDD Kata — Companion

Companion resource for [Test-Driven Development (TDD): A Practical Guide](https://qapractices.com/documentation/test-driven-development-practical-guide).

## Contents

- `kata/package.json` — Vitest 3.2 as the only devDependency; zero-config ESM setup
- `kata/src/password.js` — the validator from the guide's red-green-refactor section, extended with uppercase and digit rules
- `kata/src/fizzbuzz.js` — the final refactored FizzBuzz from the guide's step 9
- `kata/__tests__/password.test.js` — the length test from the guide plus two more rules to keep the kata going
- `kata/__tests__/fizzbuzz.test.js` — the four tests from the walkthrough, in the order they were written

## Requirements

- Node 20+
- npm

## Usage

```bash
cd kata
npm install

npm test          # Vitest 3.2 — all tests green
npm run test:watch  # watch mode: edit code, see the cycle live
npm run coverage    # v8 coverage report
```

## Replaying the red-green-refactor cycle

The point of the kata is watching tests fail before they pass:

1. Comment out a rule in `src/fizzbuzz.js` (e.g. the `isMultipleOf(n, 3)` line) and run `npm test` — the corresponding test goes **red**.
2. Restore just enough code to make it pass — **green**.
3. Try an alternative implementation (e.g. nested `if` instead of string concatenation) — the tests stay green while the design changes. That is **refactor**.

For `password.js`, each rule (length, uppercase, digit) maps to one test. Delete a rule, watch its test fail, re-add it.

See the guide for the full walkthrough, the TDD vs test-first comparison, and guidance on where the discipline fits.
