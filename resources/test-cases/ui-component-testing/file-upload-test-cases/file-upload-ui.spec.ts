import { test, expect } from '@playwright/test';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const demo = 'file://' + path.resolve(__dirname, 'upload-demo/index.html');

test.beforeEach(async ({ page }) => {
  // The demo posts to /api/upload; stub it with a delayed success.
  await page.route('**/api/upload', async (route) => {
    await new Promise((r) => setTimeout(r, 150));
    await route.fulfill({ status: 201, body: '{"id":"f-001"}' });
  });
  await page.goto(demo);
});

test('valid pdf enters the queue and completes', async ({ page }) => {
  const pdf = { name: 'report.pdf', mimeType: 'application/pdf', buffer: Buffer.from('%PDF-1.7 fake') };
  await page.setInputFiles('input[type="file"]', pdf);
  const item = page.locator('[data-testid="queue-item"]');
  await expect(item).toHaveCount(1);
  await expect(item.locator('[data-testid="status"]')).toHaveText('uploaded');
});

test('exe is rejected client-side with no request fired', async ({ page }) => {
  let posts = 0;
  await page.route('**/api/upload', (route) => { posts++; return route.fulfill({ status: 201 }); });
  const exe = { name: 'setup.exe', mimeType: 'application/x-msdownload', buffer: Buffer.from([0x4d, 0x5a]) };
  await page.setInputFiles('input[type="file"]', exe);
  await expect(page.locator('[data-testid="error"]')).toContainText('file type not allowed');
  expect(posts).toBe(0);
});

test('server 500 surfaces a retryable error state', async ({ page }) => {
  await page.unroute('**/api/upload');
  await page.route('**/api/upload', (route) => route.fulfill({ status: 500, body: 'boom' }));
  const pdf = { name: 'report.pdf', mimeType: 'application/pdf', buffer: Buffer.from('%PDF-1.7 fake') };
  await page.setInputFiles('input[type="file"]', pdf);
  await expect(page.locator('[data-testid="error"]')).toContainText('500');
  await expect(page.locator('[data-testid="retry-btn"]')).toBeVisible();
});

test('remove drops the queue entry without a request', async ({ page }) => {
  const pdf = { name: 'wrong-file.pdf', mimeType: 'application/pdf', buffer: Buffer.from('%PDF-1.7 fake') };
  await page.setInputFiles('input[type="file"]', pdf);
  await page.locator('[data-testid="remove-btn"]').click();
  await expect(page.locator('[data-testid="queue-item"]')).toHaveCount(0);
});
