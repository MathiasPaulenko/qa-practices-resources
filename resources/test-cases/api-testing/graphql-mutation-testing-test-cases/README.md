# GraphQL Mutation Testing — Runnable Companion

> Runnable companion for [GraphQL Mutation Test Cases: Create, Update & Delete](https://qapractices.com/test-cases/graphql-mutation-testing-test-cases/).

A stdlib-only mock GraphQL server plus a pytest 8.3 suite that exercises the mutation cases from the article: create/update/delete lifecycle, batch partial failure, authorization codes, error unions, idempotency-key replay and optimistic concurrency.

## Files

- `mock_server.py` — in-memory GraphQL-over-HTTP mock (`POST /graphql`) covering `createUser`, `createUsers`, `updateUser`, `deleteUser` and a `user` query. Implements non-null validation, enum checks, per-item batch results, `UNAUTHENTICATED`/`FORBIDDEN` codes, a `ValidationError` union payload, `Idempotency-Key` replay and version-based conflict detection. `run_ws()` adds a WebSocket endpoint that broadcasts `userUpdated` events on every successful update.
- `tests/` — pytest suite mapped to the article's cases:
  - `test_mutation_lifecycle.py` — TC-GQL-001 through TC-GQL-005.
  - `test_batch_and_auth.py` — TC-GQL-006, TC-GQL-007 plus non-null and enum edge rows.
  - `test_edges_and_replay.py` — TC-GQL-009, TC-GQL-010, idempotency-key replay and key-mismatch.
  - `test_subscription_trigger.py` — TC-GQL-008 (mutation → `userUpdated` event over WebSocket).
- `requirements.txt` — pinned test dependencies.

## How to use

```bash
pip install -r requirements.txt
python -m pytest tests/ -v
```

`conftest.py` starts the HTTP mock and the WebSocket endpoint on ephemeral ports per session and resets state between tests. You can also run `python mock_server.py 4000` and point `curl` or your client at `http://127.0.0.1:4000/graphql` manually.

## Requirements

- Python 3.11+
- pytest 8.3+
- requests 2.32+
- websockets 17+
