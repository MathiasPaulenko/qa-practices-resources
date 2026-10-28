import { test as base, expect, Page } from '@playwright/test';

// Custom fixture: authenticate once through the API and inject the token,
// instead of driving the login form before every test.
const test = base.extend<{ authedPage: Page }>({
  authedPage: async ({ page }, use) => {
    const response = await page.request.post('/api/login', {
      data: {
        email: process.env.QA_EMAIL || 'qa@example.com',
        password: process.env.QA_PASSWORD || 'changeme',
      },
    });
    const { token } = await response.json();

    await page.goto('/');
    await page.evaluate((t) => localStorage.setItem('authToken', t), token);
    await use(page);
  },
});

test('admin sees the admin panel', async ({ authedPage }) => {
  await authedPage.goto('/admin/dashboard');
  await expect(authedPage.getByTestId('admin-panel')).toBeVisible();
});

test('visual regression: homepage matches the baseline', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixelRatio: 0.01,
    threshold: 0.2,
  });
});
