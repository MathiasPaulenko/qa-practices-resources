# Casos de Prueba de Inventario y Stock — Archivos Companion

Companion de [Casos de Prueba de Inventario y Stock](https://qapractices.com/es/test-cases/inventory-stock-management-testing/). Un test de concurrencia ejecutable contra sobreventa, queries SQL de reposición y stock fantasma, y una suite Gherkin lista para Behave.

## Archivos

| Archivo | Propósito |
| ------- | --------- |
| `reservation_test.py` | Test de concurrencia con pytest + `requests`. Dispara 10 reservas simultáneas sobre una unidad y verifica que exactamente una tenga éxito — el invariante que detecta sobreventa. |
| `reorder_alert.sql` | Dos queries de diagnóstico: productos por debajo del umbral sin alerta, y stock fantasma (sistema > 0, almacén = 0). |
| `inventory.feature` | Escenarios Gherkin para prevención de sobreventa, expiración de reserva por TTL, alertas de reposición y asignación FEFO — listos para Behave o Cucumber. |

## Inicio Rápido

```bash
pip install pytest requests
API_BASE_URL=https://staging.yourstore.test/api pytest reservation_test.py -v
```

Sembrá `SKU123` con `stock=1` en la API destino antes de correr — el test
verifica que exactamente una reserva tenga éxito, así que una semilla más
rica lo haría pasar por el motivo equivocado.

## Requisitos

- Python 3.10+
- `pytest` 8.x, `requests` 2.32+
- Una API de inventario de staging que exponga `POST /api/reserve` (o adaptá `reserve_stock` a tus endpoints)
- Behave 1.3+ o Cucumber, si querés ejecutar `inventory.feature`
