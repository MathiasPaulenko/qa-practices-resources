# Checklist de Webhooks — Companion

Recurso companion de la [Checklist de Webhooks: Entrega, Payload y Firmas](https://qapractices.com/es/checklists/webhook-testing-checklist).

## Contenido

- `webhook-verify.mjs` — verificador de firma estilo Standard Webhooks (`{id}.{timestamp}.{payload}` con HMAC-SHA256, comparación en tiempo constante, tolerancia de 5 minutos) más el helper `sign()` correspondiente
- `receiver.mjs` — receptor HTTP mínimo que verifica la firma, deduplica por `webhook-id` y devuelve 2xx solo tras recepción durable
- `send-test-webhook.mjs` — cliente CLI que firma payloads reales y puede reenviar el mismo ID de evento para ejercitar la deduplicación
- `tests/verify.test.mjs` — suite node:test que cubre firmas válidas, payloads alterados, IDs de evento incorrectos, timestamps viejos, cabeceras ausentes, peticiones sin firmar y entrega duplicada
- `package.json` — scripts, cero dependencias de runtime

## Requisitos

- Node.js 20+ (usa `node:test` y `fetch` global, sin instalaciones)

## Uso

```bash
node --test                 # corre la suite, no hace falta servidor para los tests del verificador
node receiver.mjs           # levanta el receptor en http://localhost:3000/webhooks
node send-test-webhook.mjs --resend   # envía un evento firmado y luego repite el mismo ID de evento
```

El esquema de firma sigue la convención de [Standard Webhooks](https://github.com/standard-webhooks/standard-webhooks) que usa la checklist: el secret vive en `WEBHOOK_SECRET`, el timestamp debe estar dentro de la ventana de tolerancia, y los duplicados se responden con un 200 simple para que el emisor deje de reintentar.
