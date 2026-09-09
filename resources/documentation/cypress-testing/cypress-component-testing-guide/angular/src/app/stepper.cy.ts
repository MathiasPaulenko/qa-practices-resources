import { StepperComponent } from './stepper.component'

describe('StepperComponent', () => {
  it('mounts and displays the initial count', () => {
    cy.mount(StepperComponent, {
      componentProperties: { count: 100 },
    })
    cy.get('[data-cy="counter"]').should('have.text', '100')
  })

  it('emits the incremented value on click', () => {
    cy.mount(StepperComponent, {
      componentProperties: {
        count: 0,
        change: cy.createOutputSpy('changeSpy'),
      },
    })
    cy.get('[data-cy="increment"]').click()
    cy.get('@changeSpy').should('have.been.calledWith', 1)
  })
})
