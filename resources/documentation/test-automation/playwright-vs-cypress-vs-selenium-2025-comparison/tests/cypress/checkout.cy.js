// Cypress 13.15 — checkout flow smoke test
// Run: npx cypress run --spec tests/cypress/checkout.cy.js

describe('checkout', () => {
  beforeEach(() => {
    cy.session('checkout-user', () => {
      cy.request('POST', 'https://staging.lumapay.com/api/v1/auth/login', {
        email: 'qa@lumapay.com',
        password: Cypress.env('STAGING_PASSWORD'),
      }).then(resp => {
        window.localStorage.setItem('token', resp.body.token);
      });
    });
  });

  it('completes a payment', () => {
    cy.visit('https://staging.lumapay.com/checkout');
    cy.get('[data-testid="pay-button"]').click();
    cy.contains('Payment confirmed').should('be.visible');
  });

  it('shows error on declined card', () => {
    cy.intercept('POST', '**/api/v1/payments', { statusCode: 402, body: { error: 'card_declined' } });
    cy.visit('https://staging.lumapay.com/checkout');
    cy.get('[data-testid="pay-button"]').click();
    cy.contains('Payment failed').should('be.visible');
  });
});
