// Run: npx playwright test iframe.spec.ts  (loads fixtures via file://, no server)
import { test, expect } from '@playwright/test';
import { fileURLToPath } from 'node:url';

const host = 'file://' + fileURLToPath(new URL('./fixture-host.html', import.meta.url));

test('TC-01/07: iframe is sandboxed and has an accessible title', async ({ page }) => {
  await page.goto(host);
  const iframe = page.locator('iframe[data-testid="widget"]');
  await expect(iframe).toHaveAttribute('sandbox', /allow-scripts/);
  await expect(iframe).toHaveAttribute('title', /.+/);
});

test('TC-02: forged postMessage origin is rejected', async ({ page }) => {
  await page.goto(host);
  // forge a message with an origin not in the allowlist
  await page.evaluate(() => (window as any).forgeMessage('https://evil.example', { type: 'widget-event' }));
  await expect(page.locator('#log')).toHaveText('rejected:https://evil.example');
});

test('TC-02: legitimate widget message is accepted', async ({ page }) => {
  await page.goto(host);
  const frame = page.frameLocator('iframe[data-testid="widget"]');
  await frame.getByRole('button', { name: 'Send message to parent' }).click();
  await expect(page.locator('#log')).toHaveText('accepted:widget-event');
});
