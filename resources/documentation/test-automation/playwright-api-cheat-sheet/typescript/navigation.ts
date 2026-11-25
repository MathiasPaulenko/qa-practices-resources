// @playwright/test 1.x — page navigation and load-state waits
await page.goto('https://staging.myapp.com'); // Placeholder: replace with your staging URL
await page.goBack();
await page.goForward();
await page.reload();
await page.waitForURL('**/dashboard');
await page.waitForLoadState('networkidle');
await page.waitForLoadState('domcontentloaded');
