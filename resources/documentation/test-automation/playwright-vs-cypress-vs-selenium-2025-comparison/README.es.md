# Playwright vs Cypress vs Selenium: Comparativa 2025 — Companion

Ejemplos ejecutables de los tres frameworks de automatización de navegadores comparados en la [guía](https://qapractices.com/es/documentation/playwright-vs-cypress-vs-selenium-2025-comparison).

## Versiones

| Herramienta | Versión |
|-------------|---------|
| Playwright | 1.48.0 |
| Cypress | 13.15.0 |
| Selenium | 4.25.0 |
| Java | 21 |
| Node.js | 20.x |

## Estructura

```
tests/
├── playwright/
│   └── checkout.spec.ts    # Smoke test de checkout con Playwright 1.48
├── cypress/
│   └── checkout.cy.js      # Smoke test de checkout con Cypress 13.15
└── selenium/
    └── CheckoutTest.java   # Test JUnit 5 de checkout con Selenium 4.25
```

## Cómo correr los tests

### Playwright

```bash
npm install
npx playwright install --with-deps chromium
npm run test:playwright
```

### Cypress

```bash
npm install
npm run test:cypress
```

### Selenium

```bash
cd tests/selenium
mvn test -Dtest=CheckoutTest
```

## Notas

- Todos los tests apuntan a `https://staging.lumapay.com/checkout` como placeholder.
- Reemplazá la URL de staging y las credenciales con tu propio entorno.
- Los tests de Selenium requieren ChromeDriver que coincida con tu versión de Chrome.
