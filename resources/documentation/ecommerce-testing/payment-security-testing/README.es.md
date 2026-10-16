# Pruebas de Seguridad en Pagos — Companion Ejecutable

Repositorio companion de la guía de QAPractices
[Guía de Seguridad en Pagos: PCI DSS y Fraude](https://qapractices.com/es/documentation/payment-security-testing/)
([English version](https://qapractices.com/documentation/payment-security-testing/)).

Autocontenido: la API de pagos mock es un fixture de `http.server` de stdlib,
así que las pruebas de ataque corren sin ningún servicio externo ni
credenciales reales de pasarela.

## Estructura

```text
mock_payment_server.py          API fixture de stdlib: validación de importe en
                                servidor, deduplicación por Idempotency-Key,
                                verificación HMAC de webhooks
tests/test_payment_security.py  suite de regresión de ataques en pytest 8.2 (7 tests)
requirements.txt                requests 2.31.0, pytest 8.2.0
```

## Ejecutar la suite

```bash
python -m venv venv
source venv/bin/activate    # venv\Scripts\activate en Windows
pip install -r requirements.txt
pytest tests/test_payment_security.py -v
```

`mock_payment_server.py` arranca dentro del fixture de pytest en un puerto
efímero. Para probarlo a mano, ejecuta `python mock_payment_server.py` y
escuchará en `http://127.0.0.1:8765`.

## Qué demuestran las pruebas

| Test | Ataque simulado | Criterio de éxito |
|---|---|---|
| `test_amount_tampering_is_rejected` | El cliente envía `amount: 0.01` para un pedido de $99,99 | 400 `amount mismatch`, sin cargo creado |
| `test_currency_tampering_is_rejected` | Divisa cambiada sin recálculo | 400, sin cargo creado |
| `test_idempotent_replay_creates_single_charge` | Misma petición repetida con la misma `Idempotency-Key` | Mismo id de cargo, un solo cargo registrado |
| `test_forged_webhook_signature_is_rejected` | Evento `payment.succeeded` falso con firma basura | 401, evento no registrado |
| `test_replayed_webhook_outside_tolerance_is_rejected` | Webhook bien firmado pero con timestamp de hace 1 hora | 401 |
| `test_valid_signed_webhook_is_accepted` | Webhook correctamente firmado y reciente | 200, evento registrado |
| `test_webhook_signed_with_wrong_secret_is_rejected` | Formato válido firmado con un secreto de atacante | 401 |

El esquema de firma replica el `t=timestamp,v1=hmac_sha256` de Stripe —
cambia `WEBHOOK_SECRET` por el secreto de tu endpoint y el mismo helper
`sign_webhook` sirve para ejercitar tu endpoint real de staging.
