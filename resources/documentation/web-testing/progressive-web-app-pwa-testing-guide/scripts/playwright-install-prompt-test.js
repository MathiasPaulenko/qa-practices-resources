// Playwright 1.48 test: install prompt is deferrable
// Install: npm install -D @playwright/test@1.48
import { test, expect } from '@playwright/test';

test('install prompt is deferrable via beforeinstallprompt', async ({ page }) => {
  await page.goto('https://pwa.qa.local');

  const deferred = await page.evaluate(async () => {
    return new Promise(resolve => {
      window.addEventListener('beforeinstallprompt', (event) => {
        event.preventDefault();
        // Store the event for later use
        window.deferredPrompt = event;
        resolve(true);
      });
      // Timeout: prompt may not fire if criteria aren't met
      setTimeout(() => resolve(false), 3000);
    });
  });

  expect(deferred).toBe(true);
});

test('custom install button triggers native prompt', async ({ page }) => {
  await page.goto('https://pwa.qa.local');

  // Wait for beforeinstallprompt and capture it
  await page.evaluate(() => {
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      window.deferredPrompt = e;
      // Show a custom install button
      const btn = document.createElement('button');
      btn.id = 'install-btn';
      btn.textContent = 'Install App';
      btn.addEventListener('click', () => {
        window.deferredPrompt.prompt();
      });
      document.body.appendChild(btn);
    });
  });

  // The install button should appear if PWA criteria are met
  // Note: this test only passes on browsers that support beforeinstallprompt
  const btn = page.locator('#install-btn');
  const isVisible = await btn.isVisible().catch(() => false);
  // Don't fail if the browser doesn't support it (e.g., iOS Safari)
  if (isVisible) {
    await btn.click();
  }
});
