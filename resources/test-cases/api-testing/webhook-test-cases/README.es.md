# Casos de Prueba de Webhooks — Companion Ejecutable

Modelo determinista en Python stdlib de una entrega webhook: firma HMAC estilo Stripe (`t=<ts>,v1=<hmac_sha256(secret, "{t}.{body}")>`), un consumer que verifica, deduplica, ordena y procesa eventos, y un provider que reintenta con backoff exponencial hasta una cola dead-letter. La suite pytest mapea los TC-01..TC-12 de los [casos de prueba de webhooks](https://qapractices.com/es/test-cases/webhook-test-cases/) en qapractices.com — sin red, sin sleeps, totalmente reproducible.

## Requisitos

- Python 3.10+
- `pytest` (ver `requirements.txt`, fijado en 8.3.x)

## Ejecutar

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Archivos

| Ruta | Propósito |
|---|---|
| `webhook_pipeline.py` | `sign()`/`verify_signature()` (comparación de tiempo constante + tolerancia de timestamp), `Consumer` (firma→parseo→dedup→orden→aplicar), `Provider` (cronograma de backoff + dead-letter), `validate_endpoint()` para checks TLS |
| `tests/test_webhook_cases.py` | Un test por TC: firmas válidas/forjadas/vencidas, ventana de replay, idempotencia, fuera de orden, cronograma de backoff, payloads malformados, tipos desconocidos, rotación de secretos, validación TLS, dead-letter |
| `tests/conftest.py` | Setup de path para que los tests importen el simulador |
| `fixtures/signed-event.json` | Payload de ejemplo + cómo regenerar su header de firma |

## Qué adaptar para un provider real

- Formato del header: cambiá `SCHEME`/`sign()` por el formato del provider (`X-Hub-Signature-256: sha256=...` para GitHub, `Stripe-Signature` para Stripe).
- Tolerancia: 300 s es el default habitual; Stripe usa 5 min, configurá la tuya.
- Cronograma de reintentos: `Provider(schedule=[...])` recibe el backoff real; sumá jitter con `jitter=`.
- TTL de dedup: `Consumer.seen` es en memoria — en producción necesitás un store (Redis/DB) con TTL más largo que la ventana de reintentos del provider.
