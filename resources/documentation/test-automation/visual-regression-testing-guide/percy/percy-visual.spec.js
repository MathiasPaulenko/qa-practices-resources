import { test } from '@playwright/test';
import percySnapshot from '@percy/playwright'; // @percy/playwright 1.1.2

const BASE_URL = 'https://staging.myshop.example'; // Placeholder: replace with your staging URL

// Run with: PERCY_TOKEN=<token> npx percy exec -- playwright test percy/percy-visual.spec.js
test.describe('percy visual tests @visual', () => {
  test('homepage visual test', async ({ page }) => {
    await page.goto(BASE_URL);
    await percySnapshot(page, 'Homepage');

    await page.click('#open-modal');
    await percySnapshot(page, 'Homepage with modal');
  });
});
