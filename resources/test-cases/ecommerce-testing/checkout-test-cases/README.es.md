# Casos de Prueba de Checkout — Archivos Complementarios

Companion de [Casos de Prueba de Checkout: Pago y Envío](https://qapractices.com/es/test-cases/checkout-test-cases/). Spec de Playwright ejecutable más la matriz de tarjetas de prueba de Stripe usada en todo el recurso.

## Archivos

| Archivo | Propósito |
| ---- | ------- |
| `stripe-test-cards.csv` | Matriz de tarjetas de prueba de Stripe: número → comportamiento esperado → código de rechazo → id de escenario. Impórtala en tu suite data-driven. |
| `playwright/tests/checkout.spec.js` | Spec Playwright autocontenida (4 tests) que ejercita mensajes de rechazo, idempotencia en doble envío y el límite de envío gratis — contra un fixture HTML inline, sin backend. |

## Inicio Rápido

```bash
cd playwright
npm install
npx playwright install chromium
npm test
```

## Requisitos

- Node.js 18+
- `@playwright/test` 1.48+

La spec renderiza una página de checkout autocontenida inline (`page.setContent`), así que corre sin tienda ni pasarela. El mapa de rechazos refleja las tarjetas de prueba documentadas de Stripe — cambia el fixture por tu checkout de staging para correr los mismos casos end-to-end.
