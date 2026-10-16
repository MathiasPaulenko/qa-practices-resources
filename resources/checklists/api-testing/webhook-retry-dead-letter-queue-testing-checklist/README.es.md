# Checklist de Testing de Webhook Retry y Dead Letter Queue — Companion

Recurso companion para [Checklist de Testing de Webhook Retry y Dead Letter Queue](https://qapractices.com/es/checklists/webhook-retry-dead-letter-queue-testing-checklist).

## Contenido

- `webhook_client.py` — emisor de webhooks de referencia con backoff exponencial, jitter, soporte de `Retry-After` y una dead letter queue en memoria
- `tests/test_webhook_retry.py` — suite de pytest que cubre delays de backoff, enrutamiento de 4xx permanentes, respeto de `Retry-After`, reintentos por timeout, replay de la DLQ y rechazo de duplicados
- `requirements.txt` — dependencias de Python

## Requisitos

- Python 3.12+ con requests 2.32, responses 0.25 y pytest 8.3

## Uso

```bash
pip install -r requirements.txt
python -m pytest tests/ -v
```

Todos los tests corren contra endpoints HTTP mockeados (`responses`), así que no hace falta un receptor real. Para apuntar el cliente a un endpoint real, pasa su URL como primer argumento de `deliver_webhook()`.
