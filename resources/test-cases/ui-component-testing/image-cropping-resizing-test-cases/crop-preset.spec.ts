import { test, expect } from '@playwright/test';

// Maps to TC-28: preset selection snaps the crop area and the export honors it.
// Requires your crop UI running; adjust selectors to your app's test ids.
test('crop preset produces the advertised output size', async ({ page }) => {
  await page.goto('/crop');
  await page.setInputFiles('[data-testid="image-input"]', 'fixtures/photo.jpg');
  await page.click('[data-testid="preset-thumbnail"]');

  const selection = page.locator('[data-testid="crop-selection"]');
  const box = await selection.boundingBox();
  expect(box).not.toBeNull();
  expect(Math.abs(box!.width - box!.height)).toBeLessThanOrEqual(1);

  await page.click('[data-testid="apply-crop"]');
  const output = page.locator('[data-testid="output-image"]');
  await expect(output).toHaveAttribute('width', '150');
  await expect(output).toHaveAttribute('height', '150');
});

// Maps to TC-30: the crop area is operable without a mouse.
test('crop area responds to keyboard', async ({ page }) => {
  await page.goto('/crop');
  await page.setInputFiles('[data-testid="image-input"]', 'fixtures/photo.jpg');
  const selection = page.locator('[data-testid="crop-selection"]');
  await selection.focus();

  const before = await selection.boundingBox();
  await page.keyboard.press('ArrowRight');
  await page.keyboard.press('ArrowDown');
  const after = await selection.boundingBox();
  expect(after!.x).toBeGreaterThan(before!.x);
  expect(after!.y).toBeGreaterThan(before!.y);

  await page.keyboard.press('Enter');
  await expect(page.locator('[data-testid="output-image"]')).toBeVisible();
});
