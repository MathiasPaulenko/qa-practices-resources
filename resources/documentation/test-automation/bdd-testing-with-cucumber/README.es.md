# Cucumber BDD: JavaScript, Java y APIs Web — Companion

> Recurso companion de [Cucumber BDD: JavaScript, Java y APIs Web](https://qapractices.com/es/documentation/bdd-testing-with-cucumber) en QAPractices.com.

Feature files, step definitions en JavaScript y Java, hooks, page objects y workflow de CI para Cucumber BDD con Cucumber.js 10+ y Cucumber-JVM 7.14+.

## Requisitos

- Node.js 20+ y npm
- Java 17+ y Maven (para ejemplos en Java)
- Cucumber.js 10+ (`@cucumber/cucumber`)
- Cucumber-JVM 7.14+ (`cucumber-java`)
- Playwright (`@playwright/test`) para tests de UI
- REST Assured 5.4+ para tests de API en Java
- axios para tests de API en JavaScript

## Setup (JavaScript)

```bash
# Instalar dependencias
npm install @cucumber/cucumber @playwright/test axios

# Instalar browsers de Playwright
npx playwright install chromium

# Correr la suite BDD
npx cucumber-js --format json:results.json --format html:report.html

# Correr solo smoke tests
npx cucumber-js --tags "@smoke"

# Correr todo excepto flaky
npx cucumber-js --tags "not @flaky"
```

## Setup (Java)

```bash
# Agregar a pom.xml (ver java/pom.xml example)
mvn test

# Correr con tags
mvn test -Dcucumber.filter.tags="@smoke"
```

## Archivos

| Archivo | Propósito |
| --------- | ----------- |
| `features/authentication/login.feature` | Feature file Gherkin para autenticación de usuario |
| `features/checkout/payment.feature` | Feature file Gherkin para flujo de checkout |
| `features/api/checkout.feature` | Feature file Gherkin para checkout de API |
| `steps/loginSteps.js` | Step definitions en JavaScript para login |
| `steps/checkoutApiSteps.js` | Step definitions en JavaScript para checkout de API |
| `support/hooks.js` | Hooks de Cucumber (Before, After, BeforeAll, AfterAll) |
| `pages/LoginPage.js` | Page object para página de login |
| `.github/workflows/bdd-tests.yml` | Workflow de CI para GitHub Actions |

## Estructura de Proyecto

```text
features/
├── authentication/
│   └── login.feature
├── checkout/
│   └── payment.feature
└── api/
    └── checkout.feature

steps/
├── loginSteps.js
├── checkoutApiSteps.js
└── hooks.js

pages/
└── LoginPage.js

support/
└── world.js
```

## Licencia

MIT — libre de usar, modificar y distribuir. Nunca guardes credenciales de producción en fixtures de test; siempre usá datos sintéticos.
