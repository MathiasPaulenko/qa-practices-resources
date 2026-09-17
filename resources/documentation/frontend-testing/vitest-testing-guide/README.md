# Vitest Testing Guide — Companion

Companion resource for [Vitest Testing Guide for Modern Frontend](https://qapractices.com/documentation/vitest-testing-guide).

## Contents

- `src/calculator.ts` — Domain functions used in test examples
- `src/calculator.test.ts` — Basic test with `describe`, `it`, `expect`
- `src/mocking.test.ts` — `vi.fn()`, `vi.mock()`, `mockImplementationOnce`
- `src/snapshot.test.ts` — `toMatchSnapshot`, `toMatchInlineSnapshot`
- `vite.config.ts` — Vitest config with coverage thresholds and jsdom

## Requirements

- Node.js 18+
- Vitest 3+
- A Vite project (or the included `vite.config.ts`)

## Usage

These are reference snippets, not a runnable project. Copy the test files into your Vite project and install Vitest:

```bash
npm install --save-dev vitest@3 @vitest/ui@3
```

Add to your `vite.config.ts`:

```typescript
test: {
  globals: true,
  environment: 'jsdom',
  coverage: { provider: 'v8' },
}
```

See the guide for component tests, CI/CD integration, and common pitfalls.
