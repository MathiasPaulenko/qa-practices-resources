# API Key & Secret Management Testing — Companion Lab

Runnable lab for the [TaskFlow Example: API Key & Secret Management Testing](https://qapractices.com/test-cases/api-key-secret-management-testing/) resource on QAPractices.

A minimal Flask app reproduces the fictional TaskFlow key lifecycle: `POST /v1/api-keys` returns the full `tf_live_` key exactly once and stores only a SHA-256 hash; `GET /v1/tasks` enforces Bearer auth, scope checks, an IP allowlist and a per-key sliding-window rate limit; `revoke`, `rotate` (with grace period) and `delete` cover the end of the lifecycle; `/v1/audit-log` records `create`, `use`, `rotate`, `revoke` and `delete` events with actor and timestamp — never the secret.

## Requirements

- Python 3.10+
- `pip install -r requirements.txt`

## Run

```bash
pytest -v
```

Expected: all 13 tests pass.

## What each test verifies

| Test | Maps to | Demonstrates |
|---|---|---|
| `test_create_returns_full_key_once` | TC001 | `201` returns the raw `tf_live_` key; every later read is masked |
| `test_list_never_returns_raw_secret` | TC002 | List endpoint shows `tf_live_****…Xy9a`, never the secret |
| `test_valid_key_authenticates` | TC005 | `Bearer` key + `tasks:read` → `200 OK` |
| `test_scope_enforcement_blocks_writes` | TC006 | Read-only key → `403` on `POST /v1/tasks` |
| `test_revoked_key_fails_immediately` | TC007 | Revoked key → `401` on the next request |
| `test_deleted_key_is_gone` | TC008 | `204`, record removed, credential dead |
| `test_expired_key_rejected` | TC009 | `expires_at` in the past → `401` with expired message |
| `test_rotation_grace_period` | TC010 | New key works instantly; old key dies after grace |
| `test_rate_limit_returns_429_with_retry_after` | TC011 | Request N+1 → `429` + `Retry-After` + `X-RateLimit-*` |
| `test_ip_allowlist_blocks_unknown_source` | TC012 | Non-allowlisted IP → `403` |
| `test_key_in_query_string_rejected` | Edge table | `?api_key=` in the URL → `400` |
| `test_audit_log_has_events_without_secrets` | TC013 | `create`/`use`/`revoke` with actor; raw key absent |
| `test_generated_keys_have_entropy_and_no_collisions` | Edge table | 100 keys: unique, urlsafe alphabet, ≥32-char secret |

## Notes

- Everything runs in memory — no setup, no state between runs.
- `pytest.ini` sets `pythonpath = .` so tests import `app.py` directly.
- The raw key exists only inside the `201` creation response; the store keeps `sha256(secret)` plus the masked display value. The audit log records `key_id`, never the secret — TC013's assertion greps the whole log for the raw value.
- `GRACE_SECONDS` and `RATE_LIMIT` are module constants the tests shrink so rotation and rate-limit cases run in milliseconds.
