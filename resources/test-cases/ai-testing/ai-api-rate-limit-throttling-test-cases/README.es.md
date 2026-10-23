# Casos de Prueba para Rate Limits y Throttling en APIs de IA — Companion

Recurso companion de [Casos de Prueba para Rate Limits y Throttling en APIs de IA](https://qapractices.com/es/test-cases/ai-api-rate-limit-throttling-test-cases/).

## Contenido

- `fake_provider.py` — `http.server` de stdlib con buckets RPM por key + modelo, cuotas de tokens TPM y diarias, `Retry-After` (segundos o HTTP-date), headers estilo OpenAI `x-ratelimit-*` y modo 529 vía `X-Force-Status`. La ventana es configurable a milisegundos para probar resets sin esperar un minuto real.
- `client.py` — harness del cliente: `parse_retry_after` (delta-segundos + HTTP-date), `call_with_backoff` (respeta `Retry-After`, backoff exponencial con jitter, tope de retries) y chequeo de truncamiento SSE (sentinela `[DONE]`).
- `tests/test_rate_limits.py` — 17 tests mapeados a los TC: dentro del límite, borde exacto, ráfaga, agotamiento TPM, `Retry-After`, dispersión de jitter, tope de retries, alcance por key y por modelo, truncamiento mid-stream, degradación con fallback, manejo de 529, headers, reset de cuota, más edges de cuota diaria y HTTP-date.

## Requisitos

- Python 3.10+, `pip install -r requirements.txt`

## Uso

```bash
pytest tests/ -q
```

Salida esperada: `17 passed`.

No se consume cuota real del proveedor — cada caso corre contra el fake provider local o una sesión stubbed.

## Relacionados

- Artículo EN: https://qapractices.com/test-cases/ai-api-rate-limit-throttling-test-cases/
- Artículo ES: https://qapractices.com/es/test-cases/ai-api-rate-limit-throttling-test-cases/
