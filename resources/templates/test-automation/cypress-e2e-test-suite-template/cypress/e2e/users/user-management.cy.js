import DashboardPage from '../../support/page_objects/DashboardPage';

describe('User Management', { tags: ['regression', 'users'] }, () => {
  const dashboard = new DashboardPage();

  beforeEach(() => {
    cy.loginAsAdmin();
    dashboard.visit();
    dashboard.navigateTo('users');
  });

  it('displays user list', () => {
    cy.getByTestId('user-row').should('have.length.gte', 1);
    cy.getByTestId('user-row').first().should('contain', '@yourapp.test');
  });

  it('creates a new user', () => {
    cy.fixture('users').then((users) => {
      cy.getByTestId('add-user-button').click();
      cy.fillForm({
        'user-name': users.newUser.name,
        'user-email': users.newUser.email,
        'user-password': users.newUser.password,
      });
      cy.selectDropdown('user-role', users.newUser.role);
      cy.clickButton('Create User');

      cy.getByTestId('success-message').should('be.visible');
      cy.getByTestId('user-row').should('contain', users.newUser.email);
    });
  });

  it('edits an existing user', () => {
    cy.getByTestId('user-row').first().find('[data-testid="edit-user"]').click();
    cy.fillForm({ 'user-name': 'Updated Name' });
    cy.clickButton('Save Changes');

    cy.getByTestId('success-message').should('be.visible');
    cy.getByTestId('user-row').first().should('contain', 'Updated Name');
  });

  it('deletes a user', () => {
    cy.getByTestId('user-row').first().find('[data-testid="delete-user"]').click();
    cy.getByTestId('confirm-delete').click();

    cy.getByTestId('success-message').should('be.visible');
  });

  it('prevents duplicate email on create', () => {
    cy.fixture('users').then((users) => {
      cy.getByTestId('add-user-button').click();
      cy.fillForm({
        'user-name': 'Duplicate User',
        'user-email': users.admin.email,
        'user-password': 'AnyPass123!',
      });
      cy.clickButton('Create User');

      cy.getByTestId('error-message').should('contain', 'already exists');
    });
  });
});
