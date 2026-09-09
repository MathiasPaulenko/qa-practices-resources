import { cy } from 'cypress'
import Button from './Button'

describe('Button', () => {
  it('renders the primary variant', () => {
    cy.mount(<Button variant="primary" label="Submit" />)
    cy.get('button').should('have.text', 'Submit')
    cy.get('button').should('have.class', 'btn-primary')
  })

  it('renders a disabled state', () => {
    cy.mount(<Button variant="primary" label="Submit" disabled />)
    cy.get('button').should('be.disabled')
  })

  it('calls onClick when clicked', () => {
    const onClick = cy.spy().as('onClick')
    cy.mount(<Button variant="primary" label="Click me" onClick={onClick} />)
    cy.get('button').click()
    cy.get('@onClick').should('have.been.calledOnce')
  })
})
