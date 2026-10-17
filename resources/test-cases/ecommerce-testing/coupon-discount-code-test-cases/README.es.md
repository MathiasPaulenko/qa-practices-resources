# Casos de Prueba de Cupones y Códigos de Descuento — Archivos Complementarios

Companion de [Casos de Prueba de Cupones y Códigos de Descuento](https://qapractices.com/es/test-cases/coupon-discount-code-test-cases/). La matriz de datos de cupones, una implementación de referencia de la matemática de descuentos y una spec Playwright ejecutable.

## Archivos

| Archivo | Propósito |
| ---- | ------- |
| `coupons-test-data.csv` | Matriz de datos de prueba para los 19 códigos usados en TC001–TC033: tipo, valor, gasto mínimo, restricción de categoría, límites de uso, rango de validez, resultado esperado, TCs mapeados. |
| `discount_calc.py` | Implementación de referencia de la matemática de descuentos (basada en Decimal): porcentaje con redondeo half-up, fijo limitado al total del carrito, check de gasto mínimo pre-impuesto. Asserts auto-verificables. |
| `playwright/tests/coupon.spec.js` | Spec autocontenida (4 tests) que cubre aplicación porcentual, límite fijo al total, rechazo por gasto mínimo y no-apilamiento — contra un fixture HTML inline. |

## Inicio Rápido

```bash
python discount_calc.py          # corre los asserts para TC001/004/018/026/029
cd playwright && npm install && npx playwright test
```

## Requisitos

- Python 3.10+ (solo stdlib — `decimal`)
- Node.js 18+, `@playwright/test` 1.48+
