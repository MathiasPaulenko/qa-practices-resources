// @playwright/test 1.x — retrying web-first assertions
await expect(page.locator('#el')).toBeVisible();
await expect(page.locator('#el')).toBeHidden();
await expect(page.locator('#el')).toBeEnabled();
await expect(page.locator('#el')).toBeDisabled();
await expect(page.locator('#el')).toBeChecked();
await expect(page.locator('input')).toHaveValue('text');
await expect(page.locator('h1')).toHaveText('Title');
await expect(page.locator('h1')).toContainText('Tit');
await expect(page.locator('div')).toHaveClass(/active/);
await expect(page.locator('div')).toHaveCount(5);
await expect(page.locator('#el')).toHaveAttribute('href', '/page');
await expect(page.locator('#el')).toHaveCSS('color', 'rgb(255, 0, 0)');
await expect(page).toHaveURL(/dashboard/);
await expect(page).toHaveTitle('My App');
