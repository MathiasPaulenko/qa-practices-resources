// Intentionally flaky: the assertion runs before POST /api/cart resolves.
// This is the original GreenCart Black Friday bug — expect intermittent CI failures.
describe('add to cart (flaky)', () => {
  it('increments the cart counter', () => {
    cy.visit('/products/black-friday-bundle')
    cy.get('[data-cy="add-to-cart"]').click()
    // Race: the POST may complete before React re-renders the counter,
    // but on a fast backend the assertion still fires against the old DOM.
    cy.get('[data-cy="cart-count"]').should('contain', '1')
  })
})
