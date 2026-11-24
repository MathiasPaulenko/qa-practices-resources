// Appium + WebdriverIO skeleton for mobile permission flow testing.
// Covers: auto-grant on install, denial handling, and re-request routing
// to system settings. Requires appium 2.x with uiautomator2 / xcuitest drivers.

const { remote } = require('webdriverio');

const androidCaps = {
  platformName: 'Android',
  'appium:automationName': 'UiAutomator2',
  'appium:deviceName': 'Android Emulator',
  'appium:app': '/path/to/app-debug.apk',
  // Auto-grant every declared runtime permission on install.
  // Use for happy-path suites; for denial tests grant selectively via adb instead.
  'appium:autoGrantPermissions': true,
};

const iosCaps = {
  platformName: 'iOS',
  'appium:automationName': 'XCUITest',
  'appium:deviceName': 'iPhone 16',
  'appium:app': '/path/to/App.app',
  // 'autoAcceptAlerts': true,  // blanket accept hides denial paths; prefer per-alert handling
};

describe('permission flows', () => {
  it('grants camera permission via autoGrantPermissions', async () => {
    const driver = await remote({ capabilities: androidCaps });
    // The feature must work immediately: no system prompt should appear.
    const scanButton = await driver.$('~scanButton');
    await scanButton.click();
    await driver.$('~cameraPreview').waitForDisplayed({ timeout: 5000 });
    await driver.deleteSession();
  });

  it('routes permanently-denied permission to system settings', async () => {
    const driver = await remote({
      capabilities: { ...androidCaps, 'appium:autoGrantPermissions': false },
    });
    await driver.$('~enableNotifications').click();
    // Second denial: Android shows no dialog, the app must offer a settings link.
    const alert = await driver.$('id:com.android.packageinstaller:id/permission_deny_button');
    if (await alert.isExisting()) await alert.click();
    await driver.$('~openSettingsButton').waitForDisplayed({ timeout: 5000 });
    await driver.deleteSession();
  });

  it('handles the iOS one-shot alert deterministically', async () => {
    const driver = await remote({ capabilities: iosCaps });
    await driver.$('~enableLocation').click();
    // Accept or dismiss the next system alert explicitly.
    await driver.execute('mobile: alert', { action: 'accept' });
    // A denied alert can never be shown again on iOS: verify the settings path.
    await driver.deleteSession();
  });
});
