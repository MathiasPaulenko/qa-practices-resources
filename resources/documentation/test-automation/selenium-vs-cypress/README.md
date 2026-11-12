# Selenium vs Cypress — Companion

This companion provides runnable files for the [Selenium vs Cypress: Finova Payments Team Decision Guide](https://qapractices.com/documentation/selenium-vs-cypress).

## Files

| File | Purpose |
|------|---------|
| `tests/PaymentFlowTest.java` | Selenium 4.52 + TestNG test driving a 3-D Secure challenge in a second window |
| `tests/payment-flow.cy.ts` | Cypress 16 spec for the standard in-app card payment with `cy.intercept()` |
| `.github/workflows/selenium-regression.yml` | GitHub Actions job running only the `3dsecure` TestNG suite |
| `.github/workflows/cypress-regression.yml` | GitHub Actions job running the checkout specs without Cypress Cloud |

## Quick Start

```bash
# Selenium (Java 21 + Maven)
mvn -B test -Dsuite=3dsecure

# Cypress 16
npm install -D cypress
npx cypress run --browser chrome --spec tests/payment-flow.cy.ts
```

## Notes

The `checkout.finova.example` and `secure-provider.example` URLs are RFC 2606
placeholders — point them at your staging environment before running.

The hybrid split this guide recommends only pays off while the Selenium job
stays small (the two multi-domain flows). If the cross-domain suite grows,
re-run the decision matrix from the article.
