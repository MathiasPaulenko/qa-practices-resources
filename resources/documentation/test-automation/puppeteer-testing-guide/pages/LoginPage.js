// pages/LoginPage.js
class LoginPage {
  constructor(page) {
    this.page = page;
    this.emailSelector = '#email';
    this.passwordSelector = '#password';
    this.submitSelector = 'button[type="submit"]';
    this.errorSelector = '.error-message';
  }

  async navigate() {
    await this.page.goto('https://staging.myapp.com/login');
  }

  async login(email, password) {
    await this.page.type(this.emailSelector, email);
    await this.page.type(this.passwordSelector, password);
    await this.page.click(this.submitSelector);
  }

  async getErrorMessage() {
    await this.page.waitForSelector(this.errorSelector);
    return this.page.$eval(this.errorSelector, el => el.textContent);
  }

  async getDashboardHeading() {
    await this.page.waitForSelector('h1');
    return this.page.$eval('h1', el => el.textContent);
  }
}

module.exports = LoginPage;
