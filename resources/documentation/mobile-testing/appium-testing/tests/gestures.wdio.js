// Mobile gesture examples — WebdriverIO + Appium 2.0
// Swipe (scroll)
await driver.execute('mobile: swipeGesture', {
  elementId: await scrollable.elementId,
  direction: 'up',
  percent: 0.75
});
// Pinch to zoom
await driver.execute('mobile: pinchGesture', {
  elementId: await image.elementId,
  scale: 2.0
});
// Biometric auth (iOS Simulator)
await driver.execute('mobile: sendBiometricMatch', { match: true });
// Deep link navigation
await driver.execute('mobile: deepLink', {
  url: 'myapp://profile/settings',
  package: 'com.example.myapp'
});
