# Plan de Testing de Integración Webhook — Companion

Ejemplos ejecutables de la [Plantilla de Plan de Testing de Integración Webhook](https://qapractices.com/es/templates/webhook-integration-testing-plan-template/).

## Archivos

| Archivo | Qué hace |
|---|---|
| `verify-signature.test.js` | Verificador de firma HMAC estilo Stripe (header `t=,v1=`, tolerancia de timestamp, comparación en tiempo constante) con 6 casos `node:test`: válida, ausente, alterada, secret incorrecto, expirada, malformada. |
| `retry-simulator.js` | Simulador de retry + dead letter queue. Imprime el calendario de backoff exponencial y el resultado de seis comportamientos del receptor — incluyendo "400 nunca reintenta" y "retries agotados → DLQ". |
| `payload.sample.json` | El payload `payment.succeeded` de ejemplo usado en la Sección 2 de la plantilla. |

## Ejecutar

```bash
node --test verify-signature.test.js   # 6 tests de verificación de firma
node retry-simulator.js                # calendario de backoff + 6 escenarios de entrega
```

Sin dependencias — todo usa `node:crypto` y `node:test` (Node 18+).

## Qué demuestra

- **Verificación de firma más allá de "¿parsea?"** — la tolerancia de timestamp y la comparación en tiempo constante son las partes que los implementadores saltean y los atacantes aprovechan.
- **La matriz de retry como verdad ejecutable** — qué status codes reintentan, cuáles fallan rápido, y cuándo una entrega aterriza en la DLQ.
