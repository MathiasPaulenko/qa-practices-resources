// Cypress 13+ — companion for https://qapractices.com/documentation/cypress-best-practices/
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    testIsolation: true,
    retries: { runMode: 2, openMode: 0 },
    video: false,
    screenshotOnRunFailure: true,
    setupNodeEvents(on, config) {
      // register plugins here
    },
  },
});
