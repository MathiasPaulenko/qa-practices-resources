// support/world.js
const { setWorldConstructor } = require('@cucumber/cucumber');

class CustomWorld {
  constructor(options) {
    this.parameters = options.parameters;
    this.user = null;
    this.page = null;
    this.context = null;
    this.response = null;
    this.cartId = null;
  }

  async createAuthenticatedUser() {
    this.user = {
      email: 'test@qa.local',
      password: 'TestPass123',
      token: 'Bearer test-token'
    };
  }
}

setWorldConstructor(CustomWorld);
