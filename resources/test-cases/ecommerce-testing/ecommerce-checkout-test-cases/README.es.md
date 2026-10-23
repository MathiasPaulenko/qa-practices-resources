# Casos de Prueba de Checkout E-commerce — Motor de Carrito a Orden

Companion del recurso [Casos de Prueba de Checkout E-commerce: De Carrito a Orden](https://qapractices.com/es/test-cases/ecommerce-checkout-test-cases/) de QAPractices.

## Qué contiene

- **`checkout_flow.py`** — una máquina de estados carrito→orden en stdlib puro: líneas de carrito, cupones con subtotal mínimo y regla de un cupón por orden, umbral de envío gratis, cuentas de invitado y registradas, fusión de carrito al iniciar sesión, `place_order` idempotente con clave al estilo Stripe, órdenes, historial y consulta de invitado.
- **`tests/test_checkout_flow.py`** — 17 casos pytest mapeados 1:1 con `TC-001`..`TC-016` del recurso, más una aserción extra sobre el camino `card_declined` → HTTP 402 con carrito preservado.
- **`requirements.txt`** — solo pytest.

## Ejecución

```bash
pip install -r requirements.txt
pytest tests/ -q
```

Resultado esperado: `17 passed`.

## Mapeo

Cada test lleva el nombre del caso que verifica — `test_tc011` es el check de idempotencia del doble envío, `test_tc016` el de fuga de datos en la consulta de invitado. El gateway simulado usa los [números de tarjeta de prueba reales de Stripe](https://docs.stripe.com/testing): `4242 4242 4242 4242` aprueba, `4000 0000 0000 0002` rechaza.
