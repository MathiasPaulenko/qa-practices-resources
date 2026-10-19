import { test, expect, chromium, type BrowserContext } from '@playwright/test';
import path from 'node:path';

const pathToExtension = path.resolve(__dirname, 'extension');
let context: BrowserContext;
let extensionId: string;

test.beforeAll(async () => {
  context = await chromium.launchPersistentContext('', {
    channel: 'chromium',
    headless: false,
    args: [
      `--disable-extensions-except=${pathToExtension}`,
      `--load-extension=${pathToExtension}`,
    ],
  });
  let [worker] = context.serviceWorkers();
  if (!worker) worker = await context.waitForEvent('serviceworker');
  extensionId = worker.url().split('/')[2];
});

test.afterAll(() => context.close());

test('popup renders and persists a saved page', async () => {
  const popup = await context.newPage();
  await popup.goto(`chrome-extension://${extensionId}/popup.html`);
  await popup.click('[data-testid="save-page-btn"]');
  await expect(popup.locator('.saved-toast')).toContainText('Saved');
  const reopened = await context.newPage();
  await reopened.goto(`chrome-extension://${extensionId}/popup.html`);
  await expect(reopened.locator('.saved-item')).toHaveCount(1);
});
