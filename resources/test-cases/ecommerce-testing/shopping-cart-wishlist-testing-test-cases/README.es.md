# Testing de Shopping Cart y Wishlist — Tests y Fixtures Companion

> Recurso companion de [Testing de Shopping Cart y Wishlist](https://qapractices.com/es/test-cases/shopping-cart-wishlist-testing-test-cases) en QAPractices.com.

Specs de Playwright, helpers de API y fixtures de datos de test para testing de shopping cart y wishlist con Playwright 1.48 y pytest 8.3.

## Requisitos

- Node.js 20+
- Playwright 1.48
- Python 3.12+
- pytest 8.3
- requests 2.32

## Setup

```bash
# Instalar Playwright
npm install @playwright/test@1.48
npx playwright install

# Instalar dependencias de Python
pip install pytest==8.3 requests==2.32

# Correr tests de carrito con Playwright
npx playwright test tests/cart.spec.ts

# Correr tests de cálculo de precios por API
pytest tests/test_price_calc.py

# Correr tests de sincronización cross-device
npx playwright test tests/cross-device.spec.ts --project=mobile
```

## Archivos

| Archivo | Propósito |
| --------- | ----------- |
| `tests/cart.spec.ts` | Spec de Playwright para agregar, remover, actualizar cantidad y verificar precio |
| `tests/wishlist.spec.ts` | Spec de Playwright para agregar a wishlist, mover a carrito y validar stock |
| `tests/cross-device.spec.ts` | Spec de Playwright para sincronización cross-device del carrito |
| `tests/test_price_calc.py` | Test de pytest para subtotal, descuento, impuestos y total |
| `tests/test_inventory.py` | Test de pytest para límites de inventario y prevención de overselling |
| `fixtures/products.json` | Datos de test: SKUs, precios, niveles de stock y códigos promocionales |
| `fixtures/users.json` | Usuarios de test: autenticados, invitados y sesiones cross-device |
| `.github/workflows/cart-tests.yml` | Workflow de CI para tests de regresión de carrito y wishlist |

## Datos de Test

El directorio `fixtures/` contiene datos de test reutilizables:

- `products.json` — SKUs con precios, niveles de stock y límites por cliente
- `users.json` — usuarios autenticados, sesiones de invitado y escenarios cross-device

## Licencia

MIT — libre de usar, modificar y distribuir. Nunca testees contra sistemas de pago de producción; siempre usá tarjetas de test y usuarios sintéticos.
