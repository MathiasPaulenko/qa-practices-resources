# Testing de APIs GraphQL — Tests Companion

Companion de la guía [Pruebas de API GraphQL: Queries, Mutations y Subscriptions](https://qapractices.com/es/documentation/graphql-api-testing/). Tests ejecutables con Jest que cubren el ciclo de vida de queries y mutations, el contrato de errores de GraphQL, validación de schema por introspección, persisted queries APQ y un test de subscription por WebSocket.

## Contenido

```text
tests/
├── graphql-api.test.js    # query, mutation, contrato de errores, schema, APQ, latencia de query profunda
└── subscription.test.js   # test con cliente graphql-ws: suscribirse, disparar mutation, aseverar evento
scripts/
└── schema-diff.sh         # check de breaking changes con @graphql-inspector/cli para CI
```

## Requisitos

- Node.js 20+
- Jest 30.x, supertest 7.x, graphql 16.11+, graphql-ws 6.x, ws 8.18+
- `@graphql-inspector/cli` 7.x (solo para `scripts/schema-diff.sh`)
- Un endpoint GraphQL accesible — estos tests pegan a un servidor real, no a un mock

## Inicio rápido

```bash
npm install
export GRAPHQL_URL="https://staging.qapractices.dev"  # Placeholder: tu URL de staging
export QA_TOKEN="eyJ..."                             # JWT para los tests que requieren auth
npm test
```

Para verificar breaking changes de schema en CI:

```bash
./scripts/schema-diff.sh schema-old.graphql schema-new.graphql
```

## Notas

- Todos los tests aseveran sobre `errors[].extensions.code`, no solo sobre el status HTTP — GraphQL devuelve 200 incluso cuando fallan los resolvers.
- El test de subscription usa el protocolo `graphql-ws` (`connection_init` → `subscribe` → `next`), no el protocolo legacy de `subscriptions-transport-ws`.
- El test de APQ ejercita las dos mitades del handshake: `PersistedQueryNotFound` en la primera llamada solo con hash, y después registro y ejecución solo por hash.
