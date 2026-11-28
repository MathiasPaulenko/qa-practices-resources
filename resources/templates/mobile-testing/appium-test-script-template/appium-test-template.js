// appium-test-template.js — WebdriverIO + Appium 2.x
import { remote } from 'webdriverio';

// 1. ENVIRONMENT CONFIG — everything that changes per machine/build
const config = {
  server: 'http://127.0.0.1:4723',          // TODO: remote grid / device-farm URL in CI
  deviceName: 'TODO: e.g. Pixel_8_API_34',
  app: 'TODO: absolute path to .apk/.app, or appPackage'
};

// 2. CAPABILITIES — pick ONE variant (Android shown, iOS variant below)
const capabilities = {
  platformName: 'Android',
  'appium:automationName': 'UiAutomator2',
  'appium:deviceName': config.deviceName,
  'appium:app': config.app,
  // 'appium:appPackage': 'TODO',          // alternative to appium:app for installed apps
  // 'appium:appActivity': 'TODO',
  'appium:noReset': false                    // true = keep app state between sessions
};

// iOS variant:
// const capabilities = {
//   platformName: 'iOS',
//   'appium:automationName': 'XCUITest',
//   'appium:deviceName': config.deviceName,
//   'appium:app': config.app,
//   'appium:noReset': false
// };

// 3. SESSION SETUP
let driver;
before(async () => {
  driver = await remote({ hostname: '127.0.0.1', port: 4723, path: '/', capabilities });
});

async function waitFor(locator, timeout = 10000) {
  const el = await driver.$(locator);
  await el.waitForDisplayed({ timeout });
  return el;
}

// 4. TEST FLOW — one logical step per block
it('TODO: describes the flow under test', async () => {
  const field = await waitFor('~TODO-accessibility-id');
  await field.setValue('TODO-input');
  await (await waitFor('~TODO-button-id')).click();
  const result = await waitFor('TODO-result-locator');
  await expect(result).toHaveText('TODO-expected-text');
});

// 5. TEARDOWN — runs even if the test fails
after(async () => {
  if (driver) await driver.deleteSession();
});
