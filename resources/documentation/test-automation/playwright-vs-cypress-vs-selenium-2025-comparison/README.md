# Playwright vs Cypress vs Selenium: 2025 Comparison — Companion

Runnable examples for the three browser automation frameworks compared in the [guide](https://qapractices.com/documentation/playwright-vs-cypress-vs-selenium-2025-comparison).

## Versions

| Tool | Version |
|------|---------|
| Playwright | 1.48.0 |
| Cypress | 13.15.0 |
| Selenium | 4.25.0 |
| Java | 21 |
| Node.js | 20.x |

## Structure

```
tests/
├── playwright/
│   └── checkout.spec.ts    # Playwright 1.48 checkout smoke test
├── cypress/
│   └── checkout.cy.js      # Cypress 13.15 checkout smoke test
└── selenium/
    └── CheckoutTest.java   # Selenium 4.25 JUnit 5 checkout test
```

## Running the tests

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

## Notes

- All tests target `https://staging.lumapay.com/checkout` as a placeholder.
- Replace the staging URL and credentials with your own environment.
- The Selenium tests require ChromeDriver matching your Chrome version.
