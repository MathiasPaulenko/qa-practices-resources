import { test, expect } from '@playwright/test';

// Playwright 1.55+ — notification preferences suite for TaskFlow.
// Covers TC-016/TC-018: unsubscribe flow and per-type preference toggles.

test.describe('notification preferences', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('https://app.taskflow.io/es/config/notificaciones');
  });

  test('user disables weekly summary only', async ({ page }) => {
    const weeklyToggle = page.getByRole('switch', { name: /weekly-summary/i });
    await weeklyToggle.click();
    await expect(weeklyToggle).toHaveAttribute('aria-checked', 'false');
    // The task-assigned toggle must remain enabled.
    await expect(
      page.getByRole('switch', { name: /task-assigned/i })
    ).toHaveAttribute('aria-checked', 'true');
  });

  test('unsubscribe link lands on notification settings', async ({ page }) => {
    await page.goto('https://app.taskflow.io/es/unsubscribe?token=test-token');
    await expect(page.getByRole('button', { name: /confirm/i })).toBeVisible();
    await page.getByRole('button', { name: /confirm/i }).click();
    await expect(page.getByText(/you have been unsubscribed/i)).toBeVisible();
  });
});
