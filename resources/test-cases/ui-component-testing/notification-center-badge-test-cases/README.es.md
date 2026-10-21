# Casos de Prueba del Badge de Notificaciones — Companion

Recurso companion de [Casos de Prueba del Badge de Notificaciones: Conteo, No Leídas](https://qapractices.com/es/test-cases/notification-center-badge-test-cases/).

## Contenido

- `badge_engine.py` — modelo en Python stdlib del contador del badge: `NotificationServer` como fuente de verdad (push con dedup por id, marcar leída, marcar todas leídas, delete, expiración TTL, log de auditoría) y `BadgeTab` como la vista de una pestaña (hidratación, honestidad offline, resync tras reconexión) conectadas por un `BroadcastChannel` simulado.
- `badge.html` — fixture estático que implementa el componente real para verificación manual y con Playwright: icono de campana con elemento badge, evento `notif:push` + API `window.pushNotification`, sync entre pestañas por BroadcastChannel, mark-all-read, `aria-label` con el conteo y soporte de `prefers-reduced-motion`. Ábrelo en cualquier navegador.
- `tests/conftest.py` — pone el motor en `sys.path`.
- `tests/test_badge_engine.py` — subconjunto ejecutable de los casos del artículo: conteo de no leídas (TC-001), incremento WS (TC-002), decremento idempotente (TC-003), mark-all-read (TC-004), tope 99+ (TC-005), cero oculta (TC-006/TC-017), persistencia entre sesiones (TC-007), honestidad offline (TC-012), convergencia entre pestañas (TC-013), dedup de pushes (borde), carrera clear-vs-push (borde), delete compartido (TC-018), expiración TTL (TC-029), dedup en flood (TC-016), rastro de auditoría (TC-030) y cambio de cuenta (TC-028).

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Salida esperada: `16 passed`.

## Relacionados

- Artículo ES: https://qapractices.com/es/test-cases/notification-center-badge-test-cases/
- Artículo EN: https://qapractices.com/test-cases/notification-center-badge-test-cases/
