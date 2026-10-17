// Cypress 13+ — deterministic login spec using cy.intercept + data-cy selectors.
// Point baseUrl at a real app exposing /login and POST /api/login before running.

describe('Login', () => {
  beforeEach(() => {
    cy.intercept('POST', '/api/login').as('loginRequest');
  });

  it('logs in with valid credentials', () => {
    cy.visit('/login');
    cy.get('[data-cy=email]').type('qa.user@qapractices.dev');
    cy.get('[data-cy=password]').type('correct-horse', { log: false });
    cy.get('[data-cy=submit-login]').click();
    cy.wait('@loginRequest').its('response.statusCode').should('eq', 200);
    cy.url().should('include', '/dashboard');
  });

  it('shows an error on invalid credentials', () => {
    cy.intercept('POST', '/api/login', {
      statusCode: 401,
      body: { error: 'Invalid credentials' },
    }).as('loginFail');
    cy.visit('/login');
    cy.get('[data-cy=email]').type('qa.user@qapractices.dev');
    cy.get('[data-cy=password]').type('wrong-pass', { log: false });
    cy.get('[data-cy=submit-login]').click();
    cy.wait('@loginFail');
    cy.get('[data-cy=login-error]')
      .should('be.visible')
      .and('contain', 'Invalid credentials');
  });
});
