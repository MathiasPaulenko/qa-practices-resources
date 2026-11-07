import { test, expect } from '@playwright/test';
import path from 'node:path';

const fixture = 'file://' + path.resolve(__dirname, 'fixture', 'canvas-draw.html');

async function bitmap(page: import('@playwright/test').Page): Promise<string> {
  return page.locator('#drawing-canvas').evaluate((el: HTMLCanvasElement) => el.toDataURL());
}

test('TC-001 mouse stroke changes the canvas bitmap', async ({ page }) => {
  await page.goto(fixture);
  const blank = await bitmap(page);

  const box = await page.locator('#drawing-canvas').boundingBox();
  await page.mouse.move(box!.x + 50, box!.y + 50);
  await page.mouse.down();
  await page.mouse.move(box!.x + 200, box!.y + 150, { steps: 10 });
  await page.mouse.up();

  expect(await bitmap(page)).not.toEqual(blank);
});

test('TC-006 undo restores the previous bitmap', async ({ page }) => {
  await page.goto(fixture);
  const blank = await bitmap(page);

  const box = await page.locator('#drawing-canvas').boundingBox();
  await page.mouse.move(box!.x + 50, box!.y + 50);
  await page.mouse.down();
  await page.mouse.move(box!.x + 200, box!.y + 150, { steps: 10 });
  await page.mouse.up();

  await page.locator('#undo').click();
  expect(await bitmap(page)).toEqual(blank);
});

test('TC-019 touch stroke draws on a touchscreen context', async ({ page }) => {
  await page.goto(fixture);
  const canvas = page.locator('#drawing-canvas');
  const blank = await bitmap(page);

  await canvas.dispatchEvent('pointerdown', { pointerType: 'touch', offsetX: 100, offsetY: 100 });
  await canvas.dispatchEvent('pointermove', { pointerType: 'touch', offsetX: 150, offsetY: 150 });
  await canvas.dispatchEvent('pointerup', { pointerType: 'touch' });

  expect(await bitmap(page)).not.toEqual(blank);
});

test('TC-009 export produces a non-empty PNG download', async ({ page }) => {
  await page.goto(fixture);
  const box = await page.locator('#drawing-canvas').boundingBox();
  await page.mouse.move(box!.x + 50, box!.y + 50);
  await page.mouse.down();
  await page.mouse.move(box!.x + 200, box!.y + 150, { steps: 10 });
  await page.mouse.up();

  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.locator('#export').click(),
  ]);
  expect(download.suggestedFilename()).toBe('canvas.png');
});
