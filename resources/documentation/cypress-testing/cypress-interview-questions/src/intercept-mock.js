// cy.intercept() patterns from the guide: mock, modify, wait.
describe('network interception', () => {
  it('mocks a GET response from a fixture', () => {
    cy.intercept('GET', '/api/users', { fixture: 'users.json' }).as('getUsers')
    cy.visit('/users')
    cy.wait('@getUsers').its('response.statusCode').should('eq', 200)
  })

  it('modifies an outgoing request', () => {
    cy.intercept('POST', '/api/login', (req) => {
      req.body.password = 'mocked-password'
    }).as('login')
  })
})
