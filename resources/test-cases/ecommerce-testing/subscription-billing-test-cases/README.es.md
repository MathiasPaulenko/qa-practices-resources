# Casos de Prueba de Suscripción y Facturación — Companion

Suite pytest ejecutable para el recurso [Casos de Prueba de Suscripción y Facturación](https://qapractices.com/es/test-cases/subscription-billing-test-cases/) en QAPractices.

`conftest.py` incluye implementaciones de referencia en Python puro de la lógica de billing que más se rompe: prorrateo en céntimos enteros, schedules de dunning, idempotencia de webhooks (dedupe en el ledger), expiración de trials y reglas de estado de cancelación. La suite ejercita los casos límite — último día del ciclo, ventanas de cero días, eventos repetidos, expiración de trial sin tarjeta.

## Ejecutar

```bash
pip install -r requirements.txt
pytest tests/ -v          # 16 tests
```

## Cubre

- Prorrateo: upgrade mid-cycle, límites día 0/día 30, redondeo half-up, crédito anual→mensual
- Dunning: offsets del schedule de reintentos
- Webhooks: entrega duplicada no-op, eventos desordenados, separación cargo vs crédito
- Ciclo de vida: trial activo/expirado/con tarjeta, cancelación inmediata vs fin de período
