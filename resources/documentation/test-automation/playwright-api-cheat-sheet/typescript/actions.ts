// @playwright/test 1.x — actions auto-wait for actionability
await page.locator('#button').click();
await page.locator('#button').click({ force: true });
await page.locator('#button').dblclick();
await page.locator('#button').click({ button: 'right' });
await page.locator('input').fill('Hello World');
await page.locator('input').press('Enter');
await page.locator('input').press('Control+a');
await page.locator('select').selectOption('Option 1');
await page.locator('input').check();
await page.locator('input').uncheck();
await page.locator('input').focus();
await page.locator('input').blur();
await page.locator('textarea').scrollIntoViewIfNeeded();
await page.mouse.wheel(0, 500);
await page.locator('#source').dragTo(page.locator('#target'));
await page.locator('input').setInputFiles('path/to/file.pdf');
