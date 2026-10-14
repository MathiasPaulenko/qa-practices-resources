# Casos de Prueba de E-commerce — Spec Playwright ejecutable

Repositorio companion del recurso de QAPractices
[Casos de Prueba de E-commerce para Equipos de QA](https://qapractices.com/es/test-cases/ecommerce-test-cases/)
([English version](https://qapractices.com/test-cases/ecommerce-test-cases/)).

Autocontenido: cada fixture se renderiza inline con `page.setContent()`, así
que la spec no necesita backend de tienda. Demuestra las aserciones detrás de
los casos de carrito (TC-001 a TC-005), el caso de stock (TC-032) y el caso de
matemática de cupones (TC-034) de la suite.

## Estructura

```text
playwright/   @playwright/test 1.48.2
```

## Ejecutar

```bash
cd playwright
npm install
npx playwright test
```

La config usa `channel: 'chrome'` — corre tu Chrome instalado, así que no hace
falta descargar navegadores. Para CI, quita la opción `channel` y ejecuta
`npx playwright install chromium` para usar el navegador empaquetado.

## Qué cubre la spec

- **Agregar dos productos** — contador del carrito, líneas y subtotal `$44.49`.
- **Actualizar cantidad** — `1 → 3` recalcula el total de línea y el subtotal `$89.97`.
- **Quitar un ítem** — el otro ítem sobrevive y el subtotal baja a `$29.99`.
- **Stock cero** — el botón queda deshabilitado y dice `Out of stock`.
- **Matemática de cupones** — `SUMMER20` convierte el subtotal `$44.49` en `$35.59`;
  un código inválido reporta `Invalid coupon`.

Los cinco tests pasan en Chrome estable con Playwright 1.48.
