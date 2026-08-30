# Checklist de Pruebas de Ecommerce

> Companion imprimible de [Checklist de Pruebas de Ecommerce](https://qapractices.com/es/checklists/ecommerce-testing-checklist).

Este repositorio contiene una versión imprimible e importable de la checklist de testing de ecommerce de QAPractices.

## Archivos

- `ecommerce-testing-checklist.es.md` — Versión en Markdown, lista para imprimir o pegar en una herramienta de test management.
- `ecommerce-testing-checklist.json` — Versión estructurada en JSON con niveles de riesgo y categorías, útil para importar a Jira, TestRail, Notion o un runner de tests propio.

## Cómo usar

1. Abrí `ecommerce-testing-checklist.es.md` antes de un ciclo de release.
2. Marcá cada ítem `[x]` a medida que lo validás.
3. Ordená por **Riesgo: Alto** primero cuando el tiempo es corto.
4. Importá `ecommerce-testing-checklist.json` a tu herramienta de test management si querés test cases trackeados.

## Niveles de riesgo

- **Alto** — Seguridad, pago, inventario, PII o flujo crítico de checkout. Un fallo cuesta ingresos directamente o genera problemas de compliance.
- **Medio** — Funcionalidad importante o riesgo de regresión. Un fallo es visible pero generalmente recuperable.
- **Bajo** — Nice-to-have, accesibilidad, performance o mejoras de SEO.

## Categorías

- Catálogo de Productos
- Carrito de Compras
- Checkout
- Pagos
- Pedidos e Inventario
- Seguridad y Cumplimiento
- Performance y Móvil
- Notificaciones y SEO
- Accesibilidad
- Casos de Borde y Verificaciones Negativas
