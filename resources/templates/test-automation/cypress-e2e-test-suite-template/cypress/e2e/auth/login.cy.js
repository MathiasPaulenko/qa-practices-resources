import LoginPage from '../../support/page_objects/LoginPage';

describe('Login Flow', { tags: ['smoke', 'auth'] }, () => {
  const loginPage = new LoginPage();

  beforeEach(() => {
    loginPage.visit();
  });

  it('logs in with valid admin credentials', () => {
    cy.fixture('users').then((users) => {
      loginPage.login(users.admin.email, users.admin.password);
      cy.url().should('include', '/dashboard');
      cy.getByTestId('welcome-text').should('contain', 'Welcome');
    });
  });

  it('shows error for invalid password', () => {
    cy.fixture('users').then((users) => {
      loginPage.login(users.admin.email, 'wrongpassword');
      loginPage.getErrorMessage().should('be.visible');
      loginPage.getErrorMessage().should('contain', 'Invalid');
    });
  });

  it('shows error for empty fields', () => {
    loginPage.clickLogin();
    loginPage.getErrorMessage().should('be.visible');
    loginPage.getErrorMessage().should('contain', 'required');
  });

  it('shows error for locked account', () => {
    cy.fixture('users').then((users) => {
      loginPage.login(users.locked.email, users.locked.password);
      loginPage.getErrorMessage().should('contain', 'locked');
    });
  });

  it('navigates to forgot password', () => {
    loginPage.clickForgotPassword();
    cy.url().should('include', '/forgot-password');
  });
});
