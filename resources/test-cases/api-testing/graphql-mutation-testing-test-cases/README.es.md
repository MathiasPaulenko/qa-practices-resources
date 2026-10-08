# Testing de Mutaciones GraphQL — Companion Ejecutable

> Companion ejecutable para [Casos de Prueba de Mutaciones GraphQL](https://qapractices.com/es/test-cases/graphql-mutation-testing-test-cases/).

Un mock de servidor GraphQL escrito solo con stdlib más una suite de pytest 8.3 que ejercita los casos de mutación del artículo: ciclo de vida crear/actualizar/eliminar, fallo parcial en batch, códigos de autorización, unions de error, reintento con idempotency key y concurrencia optimista.

## Archivos

- `mock_server.py` — mock GraphQL-over-HTTP en memoria (`POST /graphql`) que cubre `createUser`, `createUsers`, `updateUser`, `deleteUser` y una query `user`. Implementa validación non-null, enums, resultados por elemento en batch, códigos `UNAUTHENTICATED`/`FORBIDDEN`, payload union `ValidationError`, reintento por `Idempotency-Key` y detección de conflicto por versión. `run_ws()` añade un endpoint WebSocket que emite eventos `userUpdated` en cada actualización correcta.
- `tests/` — suite de pytest mapeada a los casos del artículo:
  - `test_mutation_lifecycle.py` — TC-GQL-001 a TC-GQL-005.
  - `test_batch_and_auth.py` — TC-GQL-006, TC-GQL-007 y los casos edge de non-null y enum.
  - `test_edges_and_replay.py` — TC-GQL-009, TC-GQL-010, reintento de idempotency key y reutilización con payload distinto.
  - `test_subscription_trigger.py` — TC-GQL-008 (mutación → evento `userUpdated` por WebSocket).
- `requirements.txt` — dependencias de test fijadas.

## Cómo usarlo

```bash
pip install -r requirements.txt
python -m pytest tests/ -v
```

`conftest.py` levanta el mock HTTP y el endpoint WebSocket en puertos efímeros por sesión y resetea el estado entre tests. También puedes ejecutar `python mock_server.py 4000` y apuntar `curl` o tu cliente a `http://127.0.0.1:4000/graphql` manualmente.

## Requisitos

- Python 3.11+
- pytest 8.3+
- requests 2.32+
- websockets 17+
