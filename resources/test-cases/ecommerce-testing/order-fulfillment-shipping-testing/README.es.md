# Casos de Prueba de Fulfillment y Envíos

> Companion ejecutable de los [Casos de Prueba de Fulfillment y Envíos](https://qapractices.com/es/test-cases/order-fulfillment-shipping-testing/) — fixtures de webhooks estilo carrier, script de reenvío y suite pytest para los casos edge de tracking.

## Archivos

- `carrier-webhooks/` — ocho payloads de webhooks de tracking con formato de evento de carrier:
  - `01-label-created.json` → `04-delivered.json` — secuencia de camino feliz.
  - `05-out-of-order-late-ofd.json` — `out_for_delivery` tardío que llega después de `delivered`; el estado no debe retroceder.
  - `06-duplicate-in-transit.json` — replay exacto de `02` (mismo `event_id`); debe ser idempotente.
  - `07-exception-lost.json`, `08-exception-damaged.json` — eventos de excepción del carrier.
- `scripts/order_tracking_sim.py` — máquina de estados mínima que implementa las reglas bajo prueba (idempotencia, preservación del estado terminal, marcado de excepciones). Sustituye su interior por una llamada a tu handler real.
- `scripts/replay_webhooks.py` — hace POST de los fixtures a tu endpoint de webhooks e imprime el HTTP status por evento.
- `scripts/test_webhook_edges.py` — suite pytest que verifica el camino feliz, la preservación ante eventos desordenados, la idempotencia de duplicados y el manejo de excepciones.

## Cómo usarlo

1. Ejecuta la suite de casos edge contra la máquina de estados de referencia:

   ```bash
   cd scripts && pytest test_webhook_edges.py
   ```

2. Reenvía los fixtures contra tu propio receptor de webhooks:

   ```bash
   python scripts/replay_webhooks.py --base-url http://localhost:8000/webhooks/tracking
   ```

3. Reproduce el caso desordenado a mano: envía `04-delivered.json` y después `05-out-of-order-late-ofd.json` — el estado del pedido debe seguir en `delivered`.

## Requisitos

- Python 3.11+
- pytest 8.3+
- requests 2.32+ (solo para `replay_webhooks.py`; la suite pytest solo usa stdlib)

## Relacionado

- [Casos de Prueba de Fulfillment y Envíos](https://qapractices.com/es/test-cases/order-fulfillment-shipping-testing/) — la suite completa que este companion soporta (TC-04, TC-08 y la tabla de casos edge).
- [Casos de Prueba de Inventory y Stock Management](https://qapractices.com/es/test-cases/inventory-stock-management-testing/) — la disponibilidad de stock alimenta las decisiones de enrutamiento.
