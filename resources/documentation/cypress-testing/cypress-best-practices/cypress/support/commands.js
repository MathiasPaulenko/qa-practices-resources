// Cypress 12+ — session-cached login command.
// Usage: cy.login('user@domain.test', 'password') in a beforeEach.
// The session is cached after the first run, so subsequent specs skip the UI.

Cypress.Commands.add('login', (email, password) => {
  cy.session([email], () => {
    cy.visit('/login');
    cy.get('[data-cy=email]').type(email);
    cy.get('[data-cy=password]').type(password, { log: false });
    cy.get('[data-cy=submit-login]').click();
    cy.url().should('include', '/dashboard');
  });
});

// Faster variant: skip the UI entirely and log in through the API.
// Use this when the login page is not the thing under test.
Cypress.Commands.add('loginByApi', (email, password) => {
  cy.request('POST', '/api/login', { email, password }).then((response) => {
    expect(response.status).to.eq(200);
    window.localStorage.setItem('auth_token', response.body.token);
  });
});
