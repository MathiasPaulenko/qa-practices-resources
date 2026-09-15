# Mocking and Stubbing in Unit Tests — Companion

Companion resource for [Mocking and Stubbing in Unit Tests Guide](https://qapractices.com/documentation/mocking-and-stubbing-in-unit-tests-guide).

## Contents

- `src/stub_repository.ts` — Jest 30.5 stub: `mockReturnValue` on a repository
- `src/mock_logger.ts` — Jest 30.5 mock: verifying `logger.error` was called with the right message
- `src/fake_repository.ts` — In-memory fake repository implementing the `UserRepository` interface

## Requirements

- Node.js 20+
- Jest 30.5+

## Usage

These are reference snippets, not a runnable project. Copy the pattern into your own test file:

```typescript
// Stub: return a fixed value
const repo = { findById: jest.fn().mockReturnValue({ id: 1 }) };

// Mock: verify a call happened
expect(logger.error).toHaveBeenCalledWith(expect.stringContaining('Invalid'));

// Fake: in-memory implementation
const repo = new FakeUserRepository();
```

See the guide for when to use stubs vs mocks vs fakes vs spies.
