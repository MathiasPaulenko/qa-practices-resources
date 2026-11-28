// appium-login-sample.js — completed sample for a fictional e-commerce Android app
import { remote } from 'webdriverio';

const config = {
  server: 'http://127.0.0.1:4723',
  deviceName: 'Pixel_8_API_34',
  app: 'apps/shopwave-2.4.1-debug.apk'
};

const capabilities = {
  platformName: 'Android',
  'appium:automationName': 'UiAutomator2',
  'appium:deviceName': config.deviceName,
  'appium:app': config.app,
  'appium:noReset': false
};

let driver;
before(async () => {
  driver = await remote({ hostname: '127.0.0.1', port: 4723, path: '/', capabilities });
});

async function waitFor(locator, timeout = 10000) {
  const el = await driver.$(locator);
  await el.waitForDisplayed({ timeout });
  return el;
}

it('logs in with valid credentials and lands on the home screen', async () => {
  await (await waitFor('~email-input')).setValue('qa.user@shopwave.dev');
  await (await waitFor('~password-input')).setValue('Sup3rSecret!');
  await (await waitFor('~login-button')).click();
  const greeting = await waitFor('~home-greeting');
  await expect(greeting).toHaveText('Welcome back, QA User');
});

after(async () => {
  if (driver) await driver.deleteSession();
});
