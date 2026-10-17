// Example spec consuming the seeded account fixture.
import { test, expect } from './seeded-account.fixture';

test('account page loads for a seeded user', async ({ page, seededAccount }) => {
  await page.goto(`/accounts/${seededAccount.id}`);
  await expect(page.locator('h1')).toContainText(seededAccount.email);
});
