# Casos de Prueba de Notificaciones Web y Service Worker — Companion

Companion de [Casos de Prueba de Notificaciones Web y Service Worker](https://qapractices.com/es/test-cases/web-notification-service-worker-testing/) ([English version](https://qapractices.com/test-cases/web-notification-service-worker-testing/)).

## Qué incluye

- `sw.js` — un service worker fixture real que implementa los handlers que el artículo prueba: precache en `install`, purga de caché + `clients.claim()` en `activate`, fallback offline en `fetch`, `push` → `showNotification` dentro de `waitUntil`, enrutado de `notificationclick` y beacon de `notificationclose`.
- `sw_lifecycle.py` — modelo solo-stdlib de los estados del lifecycle y el pipeline push: scope de registro, rechazo en contexto inseguro, precache en install, purga de caché en activate, el ciclo waiting → `skipWaiting`, detección de update atascado, validación de payload push, expiración 410 de suscripción y limpieza en opt-out.
- `tests/test_sw_lifecycle.py` — suite pytest; cada test lleva el nombre del `TC-xx` que cubre, así un fallo apunta directo al escenario.

## Ejecutar

```bash
pip install -r requirements.txt
pytest tests/
```

## Notas

- El `sw.js` real no corre bajo pytest; úsalo como fixture de la página para la spec de Playwright del artículo (`context.serviceWorkers()` + `ServiceWorker.deliverPushMessage` por CDP en Chromium).
- En iOS, el web push solo funciona para PWAs instaladas en la Home Screen desde iOS 16.4 — ver TC-18 del artículo.
