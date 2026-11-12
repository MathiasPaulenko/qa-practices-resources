// Cypress 16: standard in-app card payment with network stubbing.
// The 3-D Secure second-tab challenge is out of scope for Cypress —
// that path stays in the Selenium TestNG suite (see PaymentFlowTest.java).
describe('Payment flow', () => {
  it('completes a standard card payment', () => {
    cy.visit('https://checkout.finova.example'); // Placeholder: replace with staging URL
    cy.get('[data-testid=card-number]').type('4111111111111111');
    cy.get('[data-testid=pay-button]').click();

    cy.intercept('POST', '/api/payments', { statusCode: 200, body: { status: 'approved' } }).as('pay');
    cy.wait('@pay');

    cy.get('[data-testid=payment-status]')
      .should('contain.text', 'Approved');
  });
});
