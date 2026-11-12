# Selenium vs Cypress — Companion

Este companion provee archivos ejecutables para la guía [Selenium vs Cypress: Guía de Decisión del Equipo Finova](https://qapractices.com/es/documentation/selenium-vs-cypress).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `tests/PaymentFlowTest.java` | Test de Selenium 4.52 + TestNG que maneja un desafío 3-D Secure en una segunda ventana |
| `tests/payment-flow.cy.ts` | Spec de Cypress 16 para el pago con tarjeta in-app usando `cy.intercept()` |
| `.github/workflows/selenium-regression.yml` | Job de GitHub Actions que corre solo la suite TestNG `3dsecure` |
| `.github/workflows/cypress-regression.yml` | Job de GitHub Actions que corre los specs de checkout sin Cypress Cloud |

## Inicio Rápido

```bash
# Selenium (Java 21 + Maven)
mvn -B test -Dsuite=3dsecure

# Cypress 16
npm install -D cypress
npx cypress run --browser chrome --spec tests/payment-flow.cy.ts
```

## Notas

Las URLs `checkout.finova.example` y `secure-provider.example` son placeholders
reservados por la RFC 2606 — apúntalas a tu entorno de staging antes de ejecutar.

La división híbrida que recomienda la guía solo compensa mientras el job de
Selenium se mantenga pequeño (los dos flujos multi-dominio). Si la suite
cross-domain crece, vuelve a correr la matriz de decisión del artículo.
