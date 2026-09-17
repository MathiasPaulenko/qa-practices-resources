const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const assert = require('node:assert/strict');

class LoginPage {
  static USERS = { 'jane@qapractices.com': 'SecurePass123!' };

  constructor() {
    this.navigateTo();
  }

  navigateTo() {
    this.email = '';
    this.password = '';
    this.message = '';
    this.onDashboard = false;
  }

  clickButton(name) {
    if (name.toLowerCase() !== 'login') return;
    if (!this.email) {
      this.message = 'Email is required';
      return;
    }
    if (!(this.email in LoginPage.USERS)) {
      this.message = 'User not found';
      return;
    }
    if (LoginPage.USERS[this.email] !== this.password) {
      this.message = 'Invalid credentials';
      return;
    }
    this.message = 'Welcome';
    this.onDashboard = true;
  }

  loginWithSso() {
    this.message = 'Welcome';
    this.onDashboard = true;
  }
}

Before(function () {
  this.page = new LoginPage();
});

After(function (scenario) {
  if (scenario.result.status === 'FAILED') {
    this.attach(`Scenario failed: ${scenario.pickle.name}`, 'text/plain');
  }
});

Given('I am on the login page', function () {
  this.page.navigateTo();
});

When('I enter {string} in the email field', function (email) {
  this.page.email = email;
});

When('I enter {string} in the password field', function (password) {
  this.page.password = password;
});

When('I click the {string} button', function (buttonName) {
  this.page.clickButton(buttonName);
});

When('I log in with SSO', function () {
  this.page.loginWithSso();
});

Then('I should see {string}', function (expectedMessage) {
  assert.equal(this.page.message, expectedMessage);
});

Then('I should be redirected to the dashboard', function () {
  assert.equal(this.page.onDashboard, true);
});

Then('I should see the dashboard', function () {
  assert.equal(this.page.onDashboard, true);
});
