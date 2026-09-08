// steps/loginSteps.js
const { Given, When, Then } = require('@cucumber/cucumber');
const { expect } = require('@playwright/test');
const { LoginPage } = require('../pages/LoginPage');

Given('a registered user with email {string} and password {string}', async function (email, password) {
  this.user = { email, password };
});

When('the user enters their credentials and clicks {string}', async function (buttonName) {
  this.loginPage = new LoginPage(this.page);
  await this.loginPage.login(this.user.email, this.user.password, buttonName);
});

When('the user enters email {string} and password {string}', async function (email, password) {
  this.user = { email, password };
  this.loginPage = new LoginPage(this.page);
  await this.loginPage.enterEmail(email);
  await this.loginPage.enterPassword(password);
});

When('clicks {string}', async function (buttonName) {
  await this.loginPage.clickButton(buttonName);
});

Then('the user should be redirected to {string}', async function (path) {
  await expect(this.page).toHaveURL(new RegExp(`.*${path}$`));
});

Then('the welcome message should display {string}', async function (message) {
  await expect(this.page.locator('[data-testid="welcome-message"]')).toHaveText(message);
});

Then('the login error message should display {string}', async function (message) {
  await expect(this.page.locator('[data-testid="login-error"]')).toHaveText(message);
});

Then('the user should remain on {string}', async function (path) {
  await expect(this.page).toHaveURL(new RegExp(`.*${path}$`));
});
