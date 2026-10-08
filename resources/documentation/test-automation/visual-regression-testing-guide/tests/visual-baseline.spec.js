import { test, expect } from '@playwright/test'; // @playwright/test 1.63.0

const BASE_URL = 'https://staging.myshop.example'; // Placeholder: replace with your staging URL

test.describe('visual regression @visual', () => {
  test('homepage matches baseline', async ({ page }) => {
    await page.goto(BASE_URL);
    await expect(page).toHaveScreenshot('homepage.png');
  });

  test('specific element matches baseline', async ({ page }) => {
    await page.goto(BASE_URL);
    const hero = page.locator('.hero-section');
    await expect(hero).toHaveScreenshot('hero.png');
  });

  test('homepage with tolerance options', async ({ page }) => {
    await page.goto(BASE_URL);
    await expect(page).toHaveScreenshot('homepage-tolerant.png', {
      maxDiffPixelRatio: 0.01, // tolerate up to 1% differing pixels
      maxDiffPixels: 100,
      threshold: 0.2, // per-pixel color sensitivity
      animations: 'disabled',
    });
  });

  test('homepage with dynamic regions masked', async ({ page }) => {
    await page.goto(BASE_URL);
    await expect(page).toHaveScreenshot('homepage-masked.png', {
      mask: [page.locator('.ad-banner'), page.locator('.timestamp')],
      maskColor: '#ff0000',
      animations: 'disabled',
    });
  });
});
