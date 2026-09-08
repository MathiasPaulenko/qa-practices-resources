// support/hooks.js
const { Before, After, BeforeAll, AfterAll } = require('@cucumber/cucumber');
const { chromium } = require('@playwright/test');

let browser;

BeforeAll(async function () {
  browser = await chromium.launch({ headless: true });
});

Before(async function ({ pickle }) {
  this.context = await browser.newContext();
  this.page = await this.context.newPage();

  if (pickle.tags.some(t => t.name === '@authenticated')) {
    await this.createAuthenticatedUser();
  }
});

After(async function ({ result }) {
  if (result.status === 'FAILED') {
    await this.page.screenshot({ path: `screenshots/${Date.now()}.png` });
  }
  await this.context.close();
});

AfterAll(async function () {
  await browser.close();
});
