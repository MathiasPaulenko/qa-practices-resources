// Fixed version: alias the request, wait on it, then assert.
describe('add to cart (fixed)', () => {
  beforeEach(() => {
    cy.session('user-session', () => {
      cy.request('POST', '/api/login', {
        email: 'priya@greencart.io',
        password: Cypress.env('TEST_PASSWORD'),
      })
    })
  })

  it('increments the cart counter', () => {
    cy.intercept('POST', '/api/cart').as('addToCart')
    cy.visit('/products/black-friday-bundle')
    cy.get('[data-cy="add-to-cart"]').click()
    cy.wait('@addToCart').its('response.statusCode').should('eq', 201)
    cy.get('[data-cy="cart-count"]').should('contain', '1')
  })
})
