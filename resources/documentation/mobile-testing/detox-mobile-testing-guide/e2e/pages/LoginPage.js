class LoginPage {
  get emailInput() { return element(by.id('email-input')) }
  get passwordInput() { return element(by.id('password-input')) }
  get loginButton() { return element(by.id('login-button')) }
  get errorMessage() { return element(by.text('Invalid credentials')) }
  get welcomeText() { return element(by.text('Welcome')) }

  async login(email, password) {
    await this.emailInput.typeText(email)
    await this.passwordInput.typeText(password)
    await this.loginButton.tap()
  }

  async expectErrorMessage() {
    await expect(this.errorMessage).toBeVisible()
  }

  async expectWelcomeVisible() {
    await expect(this.welcomeText).toBeVisible()
  }
}

module.exports = new LoginPage()
