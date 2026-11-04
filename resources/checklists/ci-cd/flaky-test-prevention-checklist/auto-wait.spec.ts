import { test, expect } from '@playwright/test';

// Playwright 1.48 auto-waiting demo from the checklist's Runnable Examples:
// assertions poll until true — no sleep(), no fixed waits.

test('submit button becomes enabled after form validation', async ({ page }) => {
  await page.goto('/signup');
  await page.fill('[name="email"]', 'valid@mail.test');
  await page.fill('[name="password"]', 'StrongPass123!');

  // toBeEnabled polls until the button is enabled or the timeout expires —
  // this is the pattern that replaces cy.wait(500) / Thread.sleep(500)
  await expect(page.locator('[data-testid="submit"]')).toBeEnabled();
});

test('anti-pattern demo: what NOT to do', async ({ page }) => {
  await page.goto('/signup');
  // BAD: await page.waitForTimeout(500); // guessing a duration
  // GOOD: wait for a condition
  await page.fill('[name="email"]', 'valid@mail.test');
  await expect(page.locator('[data-testid="submit"]')).toBeEnabled({ timeout: 5000 });
});
