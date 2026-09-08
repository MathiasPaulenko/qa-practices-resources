# Cucumber BDD: JavaScript, Java & Web APIs — Companion

> Companion resource for [Cucumber BDD: JavaScript, Java & Web APIs](https://qapractices.com/documentation/bdd-testing-with-cucumber) on QAPractices.com.

Feature files, step definitions in JavaScript and Java, hooks, page objects and CI workflow for Cucumber BDD with Cucumber.js 10+ and Cucumber-JVM 7.14+.

## Requirements

- Node.js 20+ and npm
- Java 17+ and Maven (for Java examples)
- Cucumber.js 10+ (`@cucumber/cucumber`)
- Cucumber-JVM 7.14+ (`cucumber-java`)
- Playwright (`@playwright/test`) for UI tests
- REST Assured 5.4+ for Java API tests
- axios for JavaScript API tests

## Setup (JavaScript)

```bash
# Install dependencies
npm install @cucumber/cucumber @playwright/test axios

# Install Playwright browsers
npx playwright install chromium

# Run the BDD suite
npx cucumber-js --format json:results.json --format html:report.html

# Run only smoke tests
npx cucumber-js --tags "@smoke"

# Run everything except flaky
npx cucumber-js --tags "not @flaky"
```

## Setup (Java)

```bash
# Add to pom.xml (see java/pom.xml example)
mvn test

# Run with tags
mvn test -Dcucumber.filter.tags="@smoke"
```

## Files

| File | Purpose |
| ------ | --------- |
| `features/authentication/login.feature` | Gherkin feature file for user authentication |
| `features/checkout/payment.feature` | Gherkin feature file for checkout flow |
| `features/api/checkout.feature` | Gherkin feature file for API checkout |
| `steps/loginSteps.js` | JavaScript step definitions for login |
| `steps/checkoutApiSteps.js` | JavaScript step definitions for API checkout |
| `support/hooks.js` | Cucumber hooks (Before, After, BeforeAll, AfterAll) |
| `pages/LoginPage.js` | Page object for login page |
| `.github/workflows/bdd-tests.yml` | CI workflow for GitHub Actions |

## Project Structure

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

## License

MIT — free to use, modify, and distribute. Never store production credentials in test fixtures; always use synthetic data.
