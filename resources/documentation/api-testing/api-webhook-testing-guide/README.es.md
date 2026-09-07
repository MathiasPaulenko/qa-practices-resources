# Guía de Testing de Webhooks — Scripts Companion

Recurso companion para [Guía de API Webhooks: Delivery, Retries e Integridad](https://qapractices.com/es/documentation/api-webhook-testing-guide).

## Contenido

| Archivo | Propósito |
|---------|-----------|
| `scripts/verify_signature.py` | Verificación de firma HMAC-SHA256 sobre body crudo (Python) |
| `scripts/stripe_consumer.js` | Consumidor Express con chequeo de firma, cola e idempotencia (Node.js) |
| `scripts/test_retry_behavior.py` | Simular respuestas 200/400/500/410 y verificar comportamiento de retry |
| `scripts/docker-compose.yml` | Setup local de ngrok + webhook.site para testing de integración |
| `.github/workflows/webhook-tests.yml` | Workflow de CI que corre tests de firma y retry |

## Inicio Rápido

```bash
# Levantar el consumidor de Stripe
node scripts/stripe_consumer.js

# Exponerlo con ngrok
ngrok http 3000

# Correr tests de verificación de firma
python scripts/verify_signature.py

# Correr tests de comportamiento de retry
python scripts/test_retry_behavior.py
```

## Requisitos

- Python 3.10+
- Node.js 18+
- ngrok (para testing de integración local)

## Recurso relacionado

- [Guía de API Webhooks](https://qapractices.com/es/documentation/api-webhook-testing-guide)
- [English version](https://qapractices.com/documentation/api-webhook-testing-guide)
