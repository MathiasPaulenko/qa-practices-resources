import { test, expect } from '@playwright/test';
import path from 'node:path';

const fixture = `file://${path.resolve(__dirname, 'fixture-referral.html').replace(/\\/g, '/')}`;

// Covers TC003/TC005/TC006: signup via link, conversion attributed, reward credited.
test('referral flow attributes Pro conversion to LUIS25', async ({ page }) => {
  await page.goto(`${fixture}?code=LUIS25`);
  await expect(page.locator('#cookie')).toHaveText('LUIS25');

  await page.fill('[name="email"]', 'carlos.ruiz@example.com');
  await page.click('[data-testid="signup-button"]');
  await page.click('[data-testid="complete-purchase"]');

  const status = JSON.parse(await page.locator('[data-testid="status"]').innerText());
  expect(status.referred_by).toBe('LUIS25');
  expect(status.referrer_email).toBe('luis.herrera@taskflow.io');
  expect(status.reward_status).toBe('credited');
});

// Covers TC009: self-referral via plus-alias is blocked, purchase stays organic.
test('self-referral with aliased email is flagged as fraud', async ({ page }) => {
  await page.goto(`${fixture}?code=LUIS25`);

  await page.fill('[name="email"]', 'luis.herrera+alias@taskflow.io');
  await page.click('[data-testid="signup-button"]');

  const status = JSON.parse(await page.locator('[data-testid="status"]').innerText());
  expect(status.fraud).toBe('Self-referral detected for LUIS25');
  expect(status.referred_by).toBeNull();
  await expect(page.locator('[data-testid="complete-purchase"]')).toBeDisabled();
});

// Covers TC010 edge case: without the tracking cookie the order is organic.
test('purchase without referral cookie attributes as organic', async ({ page }) => {
  await page.goto(fixture);

  await page.fill('[name="email"]', 'carlos.ruiz@example.com');
  await page.click('[data-testid="signup-button"]');
  await page.click('[data-testid="complete-purchase"]');

  const status = JSON.parse(await page.locator('[data-testid="status"]').innerText());
  expect(status.referred_by).toBeNull();
  expect(status.attribution).toBe('organic');
  expect(status.reward_status).toBeUndefined();
});
