// cypress/e2e/login.cy.js — E2E login spec
describe('Login flow', () => {
  it('logs in with valid credentials', () => {
    cy.visit('/login');
    cy.get('[data-testid="email"]').type('qa.user@example.com');
    cy.get('[data-testid="password"]').type('ValidPass123!');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/dashboard');
    cy.contains('Welcome back');
  });

  it('shows an error when the API rejects the credentials', () => {
    cy.intercept('POST', '/api/auth/login', {
      statusCode: 401,
      body: { message: 'Invalid credentials' },
    }).as('failedLogin');
    cy.visit('/login');
    cy.get('[data-testid="email"]').type('qa.user@example.com');
    cy.get('[data-testid="password"]').type('WrongPass!');
    cy.get('button[type="submit"]').click();
    cy.wait('@failedLogin');
    cy.contains('Invalid credentials').should('be.visible');
  });
});
