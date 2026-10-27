# Casos de Prueba de Notificaciones por Email — Companion

Artefactos ejecutables para el recurso [Casos de Prueba de Notificaciones por Email](https://qapractices.com/es/test-cases/email-notification-system-test-cases/) de QAPractices.

## Contenido

| Archivo | Propósito | TC relacionado |
|---|---|---|
| `sendgrid/send-test-email.sh` | Envía un email `task-assigned` por la API v3 de SendGrid | TC-001, TC-006 |
| `sendgrid/task-assigned-payload.json` | Fixture de payload del template con datos dinámicos | TC-006, TC-007 |
| `scripts/mailpit-delivery-check.sh` | Sondea un inbox Mailpit y verifica subject + header `List-Unsubscribe` | TC-009, TC-017 |
| `playwright/taskflow-notifications.spec.ts` | Esqueleto de spec para toggles de preferencias y flujo de unsubscribe (Playwright 1.55+) | TC-016, TC-018 |

## Requisitos

- `SENDGRID_API_KEY` exportada para `send-test-email.sh`.
- [Mailpit](https://mailpit.axllent.com/) v1.20+ corriendo local (`docker run -p 8025:8025 axllent/mailpit`) y `jq` para el check de entrega.
- Node 20+ y `@playwright/test` 1.55+ para el spec.

## Uso

```bash
# 1. Disparar un email contra staging/SendGrid
./sendgrid/send-test-email.sh

# 2. Verificar que llegó al inbox catch-all con los headers correctos
./scripts/mailpit-delivery-check.sh ana.martinez@taskflow.io "task assigned"

# 3. Correr el spec de UI
npx playwright test taskflow-notifications.spec.ts --reporter=list
```

English version: [README.md](README.md)
