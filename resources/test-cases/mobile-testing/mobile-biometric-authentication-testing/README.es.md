# Laboratorio de Autenticación Biométrica

Companion ejecutable de [Pruebas de Autenticación Biométrica: Face ID y Touch ID](https://qapractices.com/es/test-cases/mobile-biometric-authentication-testing/) — un modelo en Python stdlib de la máquina de estados de autenticación biométrica: intentos de match, bloqueo del SO tras cinco fallos, fallback a credencial del dispositivo, invalidación de clave por cambio de enrolamiento y expiración de sesión.

## Ejecutar

```bash
pip install -r requirements.txt
pytest -v
```

## Qué cubre

| Test | Caso de la suite |
|---|---|
| `test_successful_biometric_auth` | TC-001 camino feliz |
| `test_biometric_not_enrolled` | TC-002 opción oculta |
| `test_lockout_after_five_failures` | TC-003 bloqueo del SO |
| `test_correct_biometric_rejected_during_lockout` | TC-003 el bloqueo persiste |
| `test_second_lockout_becomes_permanent` | TC-003 bloqueo permanente |
| `test_enrollment_change_invalidates_credential` | TC-004 clave invalidada |
| `test_reenroll_after_invalidated_credential` | TC-004 credencial nueva |
| `test_backgrounding_during_prompt_returns_to_login` | TC-005 segundo plano |
| `test_no_device_security_hides_biometric` | TC-006 sin passcode |
| `test_no_sensor_reports_no_hardware` | Edge: sin sensor |
| `test_session_expiry_requires_reauth` | TC-007 timeout de sesión |
| `test_rooted_device_blocks_biometric` | TC-008 dispositivo rooteado |
| `test_device_credential_fallback` | TC-009 fallback a passcode |
| `test_wrong_passcode_does_not_clear_lockout` | TC-009 credencial incorrecta |
| `test_user_cancel_no_retry_loop` | TC-010 cancelación |
| `test_prompt_timeout` | Edge: prompt inactivo |

## Notas

- `biometric_auth.py` replica la superficie de errores de la plataforma: `LAError.biometryLockout` se convierte en `BiometricError.LOCKOUT`, `BIOMETRIC_ERROR_LOCKOUT_PERMANENT` en `LOCKOUT_PERMANENT`, y `Keychain biometryCurrentSet` / `setInvalidatedByBiometricEnrollment(true)` en el chequeo del snapshot del conjunto enrolado.
- Es un laboratorio a nivel de lógica, no un test de UI. Para cobertura en dispositivo usá `mobile:sendBiometricMatch` de Appium 2.x en emuladores, o Espresso/XCUITest en hardware real — los emuladores no reproducen ruido de sensor ni anti-spoofing.
- La política de bloqueo modela el comportamiento de iOS/Android: cinco fallos consecutivos bloquean la biometría hasta que un passcode correcto la rehabilita; un segundo ciclo de bloqueo se vuelve permanente.
