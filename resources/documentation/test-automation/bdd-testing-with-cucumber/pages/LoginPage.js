// pages/LoginPage.js
class LoginPage {
  constructor(page) {
    this.page = page;
    this.emailInput = page.locator('[data-testid="email-input"]');
    this.passwordInput = page.locator('[data-testid="password-input"]');
    this.submitButton = page.locator('[data-testid="submit-button"]');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async enterEmail(email) {
    await this.emailInput.fill(email);
  }

  async enterPassword(password) {
    await this.passwordInput.fill(password);
  }

  async clickButton(buttonName) {
    if (buttonName === 'Sign In') {
      await this.submitButton.click();
    }
  }

  async login(email, password, buttonName) {
    await this.goto();
    await this.enterEmail(email);
    await this.enterPassword(password);
    await this.clickButton(buttonName);
  }
}

module.exports = { LoginPage };
