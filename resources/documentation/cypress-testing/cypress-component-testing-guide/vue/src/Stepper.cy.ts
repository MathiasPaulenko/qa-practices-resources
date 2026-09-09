import Stepper from './Stepper.vue'

describe('Stepper', () => {
  it('increments the count', () => {
    cy.mount(Stepper)
    cy.get('[data-cy="increment"]').click()
    cy.get('[data-cy="count"]').should('contain', '1')
  })

  it('sets the initial count from props', () => {
    cy.mount(Stepper, { props: { initial: 5 } })
    cy.get('[data-cy="count"]').should('contain', '5')
  })
})
