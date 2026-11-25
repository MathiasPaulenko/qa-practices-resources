const platform = await driver.getCapabilities().platformName;
const osVersion = await driver.getCapabilities().platformVersion;

if (platform === 'Android' && parseInt(osVersion) >= 13) {
  // Handle Android 13+ granular media permissions
  await handleAndroid13Permissions(driver);
} else {
  // Handle legacy permission flow
  await handleLegacyPermissions(driver);
}
