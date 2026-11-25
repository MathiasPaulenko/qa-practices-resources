// Bad: fragile XPath
const button = await driver.$('//android.widget.Button[1]');

// Good: stable accessibility ID
const button = await driver.$('~submit-workout-button');

await driver.waitUntil(
  async () => await (await driver.$('~submit-workout-button')).isDisplayed(),
  { timeout: 15000, timeoutMsg: 'Submit button not visible within 15s' }
);
