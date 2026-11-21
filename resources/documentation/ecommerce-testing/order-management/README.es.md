# Pruebas de Gestión de Pedidos — Suite de máquina de estados e idempotencia

Suite ejecutable con pytest 8.3.4 para la [guía de pruebas de gestión de pedidos](https://qapractices.com/es/documentation/order-management/).

## Archivos

- `test_order_transitions.py` — tests parametrizados de transiciones válidas/inválidas + invariante de idempotencia del pago.
- `sample-order.json` — payload de pedido de ejemplo (totales, ítems, clave de idempotencia).

## Ejecutar

```bash
pip install pytest==8.3.4
pytest test_order_transitions.py -v
```

Los tests son autocontenidos — los stubs `FakeGateway` y `Order` simulan la captura de pago para que el invariante de idempotencia corra sin servicios externos.
