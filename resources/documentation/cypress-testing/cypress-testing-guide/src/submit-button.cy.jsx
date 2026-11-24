// src/components/SubmitButton.cy.jsx — component test with cy.mount
import SubmitButton from './SubmitButton';

it('shows loading state and disables the button', () => {
  cy.mount(<SubmitButton loading />);
  cy.get('button').should('be.disabled').and('contain', 'Saving');
});

it('emits onSubmit when clicked', () => {
  const onSubmit = cy.stub().as('onSubmit');
  cy.mount(<SubmitButton onSubmit={onSubmit} />);
  cy.get('button').click();
  cy.get('@onSubmit').should('have.been.calledOnce');
});
