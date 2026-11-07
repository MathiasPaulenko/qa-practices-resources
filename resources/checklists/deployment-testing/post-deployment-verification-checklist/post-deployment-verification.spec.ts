// Post-deployment verification spec — minimal smoke pass for the
// critical user journey right after a release.
//
// Usage:
//   BASE_URL=https://app.yourdomain.com npx playwright test post-deployment-verification.spec.ts --reporter=list
//
// Requires: @playwright/test

import { test, expect } from '@playwright/test';

const baseURL = process.env.BASE_URL || 'http://localhost:3000';

test.describe('post-deployment verification', () => {
  test('core scenario passes', async ({ request }) => {
    const res = await request.get(`${baseURL}/health`);
    expect(res.status()).toBe(200);
    const body = await res.json();
    expect(body.status).toBe('healthy');
  });

  test('critical page renders', async ({ page }) => {
    await page.goto(baseURL);
    await expect(page).not.toHaveTitle(/error|maintenance/i);
  });
});
