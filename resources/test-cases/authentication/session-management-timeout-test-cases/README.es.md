# Lab de Timeout de Sesión

Companion ejecutable de [Casos de Test de Gestión de Sesión](https://qapractices.com/es/test-cases/session-management-timeout-test-cases/) — un session store en Python solo con stdlib que replica las reglas de TaskFlow de la suite: idle timeout de 30 minutos, límite absoluto de 8 horas, access tokens de 15 minutos, rotación de refresh tokens e invalidación en el servidor al cerrar sesión, cambiar contraseña o bloquear la cuenta.

## Correr

```bash
pip install -r requirements.txt
pytest -v
```

## Qué cubre

| Test | Caso de la suite |
|---|---|
| `test_idle_timeout_expires_at_30_minutes` | TC-001 idle timeout |
| `test_activity_resets_idle_timer` | TC-002/TC-009 expiración deslizante |
| `test_refresh_issues_new_access_token` | TC-003 refresh de token |
| `test_remember_me_survives_browser_restart` | TC-004 remember me |
| `test_no_remember_me_dies_on_browser_restart` | TC-005 cookie de sesión |
| `test_concurrent_sessions_same_user` | TC-006 sesiones concurrentes |
| `test_logout_invalidates_session` | TC-008 logout |
| `test_absolute_timeout_ignores_activity` | TC-010 límite absoluto |
| `test_expired_access_token_rejected` | TC-012 token expirado |
| `test_revoked_refresh_token_rejected` | TC-013 refresh revocado |
| `test_login_regenerates_session_id` | TC-014 defensa de fijación |
| `test_password_change_kills_all_sessions` | TC-022 cambio de contraseña |
| `test_single_flight_refresh_under_concurrency` | TC-028 race de refresh |
| `test_lockout_kills_active_session` | TC-029 bloqueo |
| `test_session_cookie_flags` | TC-016/017/018 flags de cookie |

## Notas

- `session_store.py` recibe un reloj inyectable (`FakeClock` en los tests) para que los timeouts de inactividad y absolutos corran en milisegundos en vez de minutos reales.
- El refresh es single-flight: cinco threads compitiendo por el mismo refresh token producen exactamente una rotación y cuatro revocaciones — el escenario de TC-028.
- Es un lab de lógica, no un test de navegador. Para los casos de UI (TC-019/TC-020 warnings, TC-021 pestañas, TC-030 móvil en background) usa Playwright 1.48+ contra un build real de TaskFlow.
