// cypress/support/commands.js
// Custom login backed by cy.session(): authenticate once, reuse everywhere.
Cypress.Commands.add('login', (email, password) => {
  cy.session([email, password], () => {
    cy.visit('/login')
    cy.get('#email').type(email)
    cy.get('#password').type(password)
    cy.get('button[type=submit]').click()
    cy.url().should('include', '/dashboard')
  })
})
