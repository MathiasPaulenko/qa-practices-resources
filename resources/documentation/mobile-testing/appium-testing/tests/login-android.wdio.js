// wdio.conf.js capabilities section + login spec — WebdriverIO + Appium 2.0
exports.config = {
  capabilities: [{
    platformName: 'Android',
    'appium:deviceName': 'Pixel_7_API_34',
    'appium:automationName': 'UiAutomator2',
    'appium:app': '/path/to/app.apk', // placeholder: path to your build artifact
    'appium:noReset': false
  }],
  services: ['appium']
};

describe('Login Flow', () => {
  it('should log in with valid credentials', async () => {
    const username = await $('~username-input');
    await username.setValue('test@example.com');
    const password = await $('~password-input');
    await password.setValue('SecurePass123');
    const loginBtn = await $('~login-button');
    await loginBtn.click();
    const dashboard = await $('~dashboard-welcome');
    await expect(dashboard).toBeDisplayed();
  });
});
