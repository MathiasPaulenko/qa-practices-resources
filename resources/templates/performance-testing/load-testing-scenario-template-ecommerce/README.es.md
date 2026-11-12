# Escenario de Load Testing — Checkout E-commerce (companion)

Companion ejecutable de la [plantilla de Escenario de Load Testing](https://qapractices.com/es/templates/load-testing-scenario-template-ecommerce).

## Contenido

- `scripts/checkout-journey.js` — script k6 del journey de checkout (executor ramping-vus, thresholds por journey, usuarios de prueba por VU desde `data/test-users.json`).
- `data/test-users.json` — pool de usuarios para que los VUs no compartan sesión (ver la tabla de Escenarios Negativos de la plantilla).
- `scenario-config.json` — perfil de tráfico, mix de journeys y umbrales que reflejan las Secciones 2, 4 y 6 de la plantilla.

## Ejecución

```bash
k6 run -e BASE_URL=https://staging.tu-app.internal scripts/checkout-journey.js
```

Requisitos: k6 0.55+. Apunta `BASE_URL` a un entorno de staging — nunca producción, y usa la pasarela de pago en sandbox.
