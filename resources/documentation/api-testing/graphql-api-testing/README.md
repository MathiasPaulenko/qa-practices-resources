# GraphQL API Testing — Companion Tests

Companion for the [GraphQL API Testing: Queries, Mutations & Subscriptions](https://qapractices.com/documentation/graphql-api-testing/) guide. Runnable Jest tests covering the query/mutation lifecycle, the GraphQL error contract, schema validation via introspection, APQ persisted queries and a WebSocket subscription test.

## Contents

```text
tests/
├── graphql-api.test.js    # query, mutation, error contract, schema, APQ, deep-query latency
└── subscription.test.js   # graphql-ws client test: subscribe, trigger mutation, assert event
scripts/
└── schema-diff.sh         # @graphql-inspector/cli breaking-change check for CI
```

## Requirements

- Node.js 20+
- Jest 30.x, supertest 7.x, graphql 16.11+, graphql-ws 6.x, ws 8.18+
- `@graphql-inspector/cli` 7.x (only for `scripts/schema-diff.sh`)
- A reachable GraphQL endpoint — these tests hit a live server, not a mock

## Quick start

```bash
npm install
export GRAPHQL_URL="https://staging.qapractices.dev"  # Placeholder: your staging URL
export QA_TOKEN="eyJ..."                             # JWT for auth-required tests
npm test
```

To check for breaking schema changes in CI:

```bash
./scripts/schema-diff.sh schema-old.graphql schema-new.graphql
```

## Notes

- Every test asserts on `errors[].extensions.code`, not just HTTP status — GraphQL returns 200 even on resolver failures.
- The subscription test uses the `graphql-ws` protocol (`connection_init` → `subscribe` → `next`), not the legacy `subscriptions-transport-ws` protocol.
- The APQ test exercises both halves of the handshake: `PersistedQueryNotFound` on hash-only first call, then registration and hash-only execution.
