# Casos de Prueba de Notificaciones Push — Archivos Complementarios

Companion de [Casos de Prueba de Notificaciones Push: Entrega, Permisos](https://qapractices.com/es/test-cases/push-notification-test-cases/). Payloads reales por proveedor y un script de verificación del ciclo de vida del token.

## Archivos

| Archivo | Propósito |
| ---- | ------- |
| `payloads/fcm-notification.json` | Mensaje de notificación FCM HTTP v1: título/cuerpo, deep link en data, canal Android + prioridad HIGH, alerta APNs con thread-id. |
| `payloads/fcm-data-silent.json` | Push solo-datos (silencioso): prioridad NORMAL de FCM, `content-available: 1` de APNs + `apns-push-type: background`. |
| `payloads/web-push.json` | Payload de web push con tag/renotify, icon/badge, acciones y `data.url` de deep link — coincide con TC015/TC016. |
| `check_token_lifecycle.sh` | Checks del ciclo de vida del token siguiendo TC003/004/005: registro existe, re-registro idempotente, sonda de purga de token obsoleto. |

## Uso

```bash
chmod +x check_token_lifecycle.sh
API_BASE="https://tu-api" AUTH="Bearer $TOKEN" ./check_token_lifecycle.sh <device_id>
```

Envía los payloads con `POST https://fcm.googleapis.com/v1/projects/YOUR_PROJECT/messages:send` (FCM v1) o tu librería de web-push preferida.

## Requisitos

- `bash`, `curl`, Python 3 (para parsear JSON en el script)
- Un backend con endpoints de push-tokens — adapta las rutas a tu API
