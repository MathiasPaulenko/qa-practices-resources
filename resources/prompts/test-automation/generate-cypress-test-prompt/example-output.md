# Example Output — Checkout E2E Suite (excerpt)

## File tree

```text
cypress/e2e/
  checkout/
    checkout.cy.js
    selectors.js
  fixtures/
    products.json
    users.json
```

## selectors.js

```javascript
export const selectors = {
  emailInput: '[data-testid="email-input"]',
  passwordInput: '[data-testid="password-input"]',
  loginButton: '[data-testid="login-button"]',
  addToCartButton: '[data-testid="add-to-cart"]',
  cartBadge: '[data-testid="cart-badge"]',
  checkoutButton: '[data-testid="checkout-button"]',
  confirmationMessage: '[data-testid="confirmation-message"]'
};
```

## checkout.cy.js

```javascript
import { selectors } from './selectors';

describe('Checkout Flow', () => {
  beforeEach(() => {
    cy.login('qa@testmail.dev', 'TestPass123!');
    cy.intercept('GET', '/api/products', { fixture: 'products' }).as('getProducts');
    cy.visit('/products');
    cy.wait('@getProducts');
  });

  it('completes a purchase with valid payment', () => {
    cy.get(selectors.addToCartButton).click();
    cy.get(selectors.checkoutButton).click();
    cy.intercept('POST', '/api/orders').as('createOrder');
    cy.get('[data-testid="place-order"]').click();
    cy.wait('@createOrder').its('response.statusCode').should('eq', 201);
    cy.get(selectors.confirmationMessage).should('be.visible');
  });

  it('rejects checkout with an empty cart', () => {
    cy.get(selectors.checkoutButton).click();
    cy.get('[data-testid="error-message"]')
      .should('be.visible')
      .and('contain', 'Your cart is empty');
  });

  it('shows an error when the order API fails', () => {
    cy.get(selectors.addToCartButton).click();
    cy.get(selectors.checkoutButton).click();
    cy.intercept('POST', '/api/orders', { statusCode: 500 }).as('createOrderFail');
    cy.get('[data-testid="place-order"]').click();
    cy.wait('@createOrderFail');
    cy.get('[data-testid="error-message"]')
      .should('be.visible')
      .and('contain', 'Something went wrong');
  });
});
```

## fixtures/users.json

```json
{
  "standardUser": { "email": "qa@testmail.dev", "password": "TestPass123!" },
  "adminUser": { "email": "admin@testmail.dev", "password": "AdminPass456!" }
}
```
