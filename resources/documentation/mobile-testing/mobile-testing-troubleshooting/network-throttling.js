// BrowserStack network throttling
const networkProfile = '4g'; // '2g', '3g', '4g', 'offline', 'intermittent'
await driver.setNetworkConnection(networkProfile);
await driver.pause(2000); // Allow condition to stabilize
// Now trigger the app action
await (await driver.$('~sync-workout-button')).click();
