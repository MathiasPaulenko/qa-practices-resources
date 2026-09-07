const { By, until } = require('selenium-webdriver');

class LoginPage {
  constructor(driver) {
    this.driver = driver;
  }

  async open() {
    await this.driver.get('https://staging.qa.local/login');
  }

  async login(email, password) {
    await this.driver.findElement(By.id('email')).sendKeys(email);
    await this.driver.findElement(By.id('password')).sendKeys(password);
    await this.driver.findElement(By.css("[data-testid='login-button']")).click();
    await this.driver.wait(until.urlContains('/dashboard'), 5000);
  }

  async getErrorMessage() {
    const el = await this.driver.wait(
      until.elementLocated(By.id('error')),
      5000
    );
    return el.getText();
  }
}

module.exports = { LoginPage };
