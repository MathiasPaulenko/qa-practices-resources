// @playwright/test 1.x — explicit waits and default timeout
await page.locator('#el').waitFor({ state: 'visible' });
await page.locator('#el').waitFor({ state: 'attached' });
await page.locator('#el').waitFor({ state: 'detached' });
await page.locator('#el').waitFor({ timeout: 10000 });

// Set default timeout
page.setDefaultTimeout(10000);
