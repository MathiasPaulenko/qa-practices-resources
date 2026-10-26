# Casos de Prueba de Autenticación de Dos Factores — Companion

Materiales ejecutables para el recurso [Casos de Prueba de Autenticación de Dos Factores (2FA)](https://qapractices.com/es/test-cases/two-factor-authentication-test-cases/) de QAPractices.

## Contenido

| Archivo | Qué es |
|---|---|
| `totp_service.py` | Servicio TOTP sin dependencias: generación y verificación RFC 6238 (HMAC-SHA-1, pasos de 30s, 6 dígitos), uso único, bloqueo a los 5 intentos, deriva de reloj configurable y códigos de respaldo de un solo uso. |
| `webauthn_service.py` | Simulador de ceremonias WebAuthn: emisión de challenges con TTL de 60s, challenges de un solo uso, origin binding, registro y revocación de credenciales — la máquina de estados del lado servidor detrás de TC-014, sin cripto de attestation real. |
| `login_gateway.py` | Gateway de login 2FA mínimo: el login por contraseña solo emite un token pre-auth mientras el 2FA está pendiente, los flags de bypass del cliente se ignoran, los códigos están ligados a la cuenta que los pidió y hay enforcement por rol con `2fa_enrollment_required` (TC-015, TC-016). |
| `test_two_factor.py` | Suite pytest mapeada a los casos TC-###: código válido, código incorrecto, replay, ventana expirada, tolerancia de deriva, bloqueo rechazando códigos válidos, consumo y agotamiento de códigos de respaldo, entropía del secreto. |
| `test_webauthn.py` | Suite pytest para TC-014 y el edge case de timeout de ceremonia: challenge de enrolamiento, aserción exitosa, rechazo por origen incorrecto, revocación, challenges expirados y reutilizados. |
| `test_login_gateway.py` | Suite pytest para TC-015/016: estado pre-auth en vez de sesión, flags inyectados `2fa_verified`/`skip_2fa` ignorados, token pre-auth rechazado en rutas autenticadas, rechazo de código de otra cuenta y enforcement de enrolamiento para admin. |
| `requirements.txt` | Solo `pytest` — los servicios son stdlib puro (`hmac`, `hashlib`, `base64`, `secrets`, `struct`, `time`). |

## Inicio rápido

```bash
pip install -r requirements.txt
pytest -v
```

Prueba el servicio directamente:

```bash
python -c "
from totp_service import TOTPService
svc = TOTPService()
secret = svc.generate_secret('alice@example.com', issuer='UrbanThreads')
code = svc.current_code(secret)
print(secret, code, svc.verify(secret, code))
"
```

## Notas

- `verify(secret, code, at=...)` acepta un timestamp falso, así que los tests pueden ejercitar la expiración de ventana y la deriva ±1-paso sin dormir.
- `MAX_ATTEMPTS` bloquea la cuenta a los 5 fallos — y un código válido sigue rechazado estando bloqueada, como pide el resultado esperado de TC-007.
- Los códigos de respaldo viven en un set y se eliminan al usarse; `remaining_backup_codes()` expone el agotamiento para TC-006.
- El parámetro drift está apagado por defecto (`drift=0`): aceptar una ventana adyacente es una decisión de política documentada, no un default silencioso.
- `WebAuthnService` valida frescura del challenge, tipo y origen antes de consumirlo — el mismo orden que un RP real usa al validar `clientDataJSON`. Pasa `origin=` para ejercitar el rechazo por origin binding del paso 4 de TC-014.
- `LoginGateway.login()` acepta flags keyword arbitrarios a propósito: pasar `2fa_verified=True` o `skip_2fa=True` debe seguir devolviendo el estado pre-auth, que es exactamente lo que TC-015 verifica.
