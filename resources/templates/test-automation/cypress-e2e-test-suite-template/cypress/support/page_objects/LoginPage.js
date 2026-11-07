class LoginPage {
  visit() {
    cy.visit('/login');
    return this;
  }

  fillEmail(email) {
    cy.getByTestId('email').clear().type(email);
    return this;
  }

  fillPassword(password) {
    cy.getByTestId('password').clear().type(password);
    return this;
  }

  clickLogin() {
    cy.getByTestId('login-button').click();
    return this;
  }

  login(email, password) {
    this.fillEmail(email);
    this.fillPassword(password);
    this.clickLogin();
    return this;
  }

  getErrorMessage() {
    return cy.getByTestId('error-message');
  }

  clickForgotPassword() {
    cy.getByTestId('forgot-password').click();
    return this;
  }

  isLoaded() {
    cy.getByTestId('login-button').should('be.visible');
    return this;
  }
}

export default LoginPage;
