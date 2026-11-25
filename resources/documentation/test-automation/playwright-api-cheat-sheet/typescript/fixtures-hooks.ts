// @playwright/test 1.x — built-in page fixture and shared setup hooks
test.beforeEach(async ({ page }) => {
  await page.goto('/login');
  await page.locator('#email').fill('test@test.com');
  await page.locator('#password').fill('password');
  await page.locator('#submit').click();
});

test.afterEach(async ({ page }) => {
  await page.close();
});

test('dashboard loads', async ({ page }) => {
  await page.goto('/dashboard');
  await expect(page.locator('h1')).toHaveText('Dashboard');
});
