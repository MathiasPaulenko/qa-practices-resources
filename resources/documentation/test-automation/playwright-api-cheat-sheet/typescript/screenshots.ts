// @playwright/test 1.x — page and element screenshots
await page.screenshot({ path: 'screenshot.png' });
await page.screenshot({ path: 'full.png', fullPage: true });
await page.locator('#el').screenshot({ path: 'element.png' });
