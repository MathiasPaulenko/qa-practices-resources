describe('3DS challenge for Adyen', () => {
  it('completes payment', () => {
    cy.visit('/checkout');
    cy.get('[data-testid=card-number]').type('4111 1111 1111 1111');
    cy.get('[data-testid=pay-button]').click();

    // Cross-origin 3DS iframes aren't native in Cypress
    cy.iframe('[name=threeds-challenge]').find('#password').type('password');
    cy.iframe('[name=threeds-challenge]').find('#submit').click();

    cy.contains('Payment successful').should('be.visible');
  });
});