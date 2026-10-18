# Testing de Gestión de API Keys y Secretos — Lab Companion

Lab ejecutable del recurso [Ejemplo TaskFlow: Testing de Gestión de API Keys y Secretos](https://qapractices.com/es/test-cases/api-key-secret-management-testing/) de QAPractices.

Una app Flask mínima reproduce el ciclo de vida de keys de la ficticia TaskFlow: `POST /v1/api-keys` devuelve la key `tf_live_` completa una única vez y guarda solo un hash SHA-256; `GET /v1/tasks` aplica auth Bearer, chequeo de scopes, allowlist de IP y rate limit por key con ventana deslizante; `revoke`, `rotate` (con período de gracia) y `delete` cubren el final del ciclo; `/v1/audit-log` registra eventos `create`, `use`, `rotate`, `revoke` y `delete` con actor y timestamp — nunca el secreto.

## Requisitos

- Python 3.10+
- `pip install -r requirements.txt`

## Ejecutar

```bash
pytest -v
```

Esperado: los 13 tests pasan.

## Qué verifica cada test

| Test | Mapea a | Demuestra |
|---|---|---|
| `test_create_returns_full_key_once` | TC001 | `201` devuelve la key cruda; toda lectura posterior va enmascarada |
| `test_list_never_returns_raw_secret` | TC002 | El listado muestra `tf_live_****…Xy9a`, nunca el secreto |
| `test_valid_key_authenticates` | TC005 | Key `Bearer` + `tasks:read` → `200 OK` |
| `test_scope_enforcement_blocks_writes` | TC006 | Key de solo lectura → `403` en `POST /v1/tasks` |
| `test_revoked_key_fails_immediately` | TC007 | Key revocada → `401` en el request siguiente |
| `test_deleted_key_is_gone` | TC008 | `204`, registro eliminado, credencial muerta |
| `test_expired_key_rejected` | TC009 | `expires_at` vencido → `401` con mensaje de expiración |
| `test_rotation_grace_period` | TC010 | La key nueva funciona al instante; la vieja muere tras la gracia |
| `test_rate_limit_returns_429_with_retry_after` | TC011 | El request N+1 → `429` + `Retry-After` + `X-RateLimit-*` |
| `test_ip_allowlist_blocks_unknown_source` | TC012 | IP fuera de la allowlist → `403` |
| `test_key_in_query_string_rejected` | Tabla edge | `?api_key=` en la URL → `400` |
| `test_audit_log_has_events_without_secrets` | TC013 | `create`/`use`/`revoke` con actor; la key cruda ausente |
| `test_generated_keys_have_entropy_and_no_collisions` | Tabla edge | 100 keys: únicas, alfabeto urlsafe, secreto ≥32 chars |

## Notas

- Todo corre en memoria — sin setup y sin estado entre ejecuciones.
- `pytest.ini` define `pythonpath = .` para que los tests importen `app.py` directamente.
- La key cruda solo existe dentro de la respuesta `201` de creación; el store guarda `sha256(secret)` más el valor enmascarado. El audit log registra `key_id`, nunca el secreto — la aserción de TC013 hace grep de todo el log buscando el valor crudo.
- `GRACE_SECONDS` y `RATE_LIMIT` son constantes de módulo que los tests reducen para que los casos de rotación y rate limit corran en milisegundos.
