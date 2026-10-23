# Casos de Prueba de Autenticación de Dos Factores — Companion

Materiales ejecutables para el recurso [Casos de Prueba de Autenticación de Dos Factores (2FA)](https://qapractices.com/es/test-cases/two-factor-authentication-test-cases/) de QAPractices.

## Contenido

| Archivo | Qué es |
|---|---|
| `totp_service.py` | Servicio TOTP sin dependencias: generación y verificación RFC 6238 (HMAC-SHA-1, pasos de 30s, 6 dígitos), uso único, bloqueo a los 5 intentos, deriva de reloj configurable y códigos de respaldo de un solo uso. |
| `test_two_factor.py` | Suite pytest mapeada a los casos TC-###: código válido, código incorrecto, replay, ventana expirada, tolerancia de deriva, bloqueo rechazando códigos válidos, consumo y agotamiento de códigos de respaldo, entropía del secreto. |
| `requirements.txt` | Solo `pytest` — el servicio es stdlib puro (`hmac`, `hashlib`, `base64`, `secrets`, `struct`, `time`). |

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
