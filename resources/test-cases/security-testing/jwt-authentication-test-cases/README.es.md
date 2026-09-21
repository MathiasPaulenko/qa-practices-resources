# Casos de Prueba de Autenticación JWT — Lab Companion

Lab ejecutable del recurso [Casos de Prueba de Autenticación JWT](https://qapractices.com/es/test-cases/jwt-authentication-test-cases/) de QAPractices.

Una app Flask mínima emite pares access + refresh token RS256 y expone el mismo endpoint de perfil dos veces: `/secure/api/profile` verifica correctamente (algoritmo fijado, claims completos, denylist de `jti`) mientras `/vulnerable/api/profile` confía en el header `alg` del propio token — el bug detrás de `alg=none` y la confusión RS256→HS256 — y nunca consulta la denylist. La suite pytest dispara los ataques del recurso contra ambos y verifica la diferencia observable.

## Requisitos

- Python 3.10+
- `pip install -r requirements.txt`

## Ejecutar

```bash
pytest -v
```

Esperado: los 10 tests pasan. Cada test documenta el comportamiento vulnerable *y* el protegido — la suite está en verde porque ambos lados se comportan como se diseñaron.

## Qué verifica cada test

| Test | Corresponde a | Demuestra |
|---|---|---|
| `test_valid_token_grants_access_on_secure` | TC-JWT-001 | Token firmado correctamente y sin expirar → HTTP 200 |
| `test_expired_token_rejected_on_both` | TC-JWT-002 | `exp` en el pasado → HTTP 401 en ambos verificadores |
| `test_tampered_payload_rejected_on_both` | TC-JWT-003 | `role` cambiado a `admin` sin refirmar → HTTP 401 |
| `test_alg_none_accepted_on_vulnerable` | TC-JWT-004 | Token `alg=none` sin firmar → HTTP 200 como `admin` |
| `test_alg_none_rejected_on_secure` | TC-JWT-004 | El mismo token → HTTP 401 |
| `test_rs256_as_hs256_accepted_on_vulnerable` | TC-JWT-005 | Token firmado con la clave pública como secreto HMAC → HTTP 200 |
| `test_rs256_as_hs256_rejected_on_secure` | TC-JWT-005 | El mismo token forjado → HTTP 401 |
| `test_refresh_rotation_and_replay_rejected` | TC-JWT-007 | El primer intercambio rota; reutilizar el token consumido revoca toda la familia |
| `test_revoked_token_rejected_on_secure` | Tabla edge | El logout mete el `jti` en la denylist → el replay devuelve 401 |
| `test_revoked_token_still_valid_on_vulnerable` | Tabla edge | Sin denylist → el mismo token sigue funcionando hasta `exp` |

## Notas

- Las claves se generan al importar — sin setup, sin estado entre ejecuciones.
- `pytest.ini` define `pythonpath = .` para que los tests importen `app.py` directamente.
- PyJWT 2.x se niega a usar una clave asimétrica como secreto HMAC, así que la forja de confusión firma el token a mano con `hmac` — exactamente como funciona el ataque real.
- El código vulnerable existe solo para formación. Nunca dejes que el header `alg` del token elija tu clave de verificación.
