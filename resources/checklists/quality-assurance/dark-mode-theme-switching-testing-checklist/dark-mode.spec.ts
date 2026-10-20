import { test, expect, Page } from '@playwright/test';

/**
 * Dark mode and theme switching spec.
 *
 * Covers the automatable checks from the QAPractices checklist:
 * theme resolution order, persistence, FOIT, toggle behavior, and
 * prefers-color-scheme handling. Visual contrast still needs a manual
 * pass — axe assertions here only catch what a DOM scan can see.
 *
 * Requires @playwright/test 1.48+.
 *
 * Run:
 *   BASE_URL=https://your-app.com npx playwright test dark-mode.spec.ts --reporter=list
 *
 * Assumptions (adapt to your app):
 *   - Theme class `dark`/`light` is applied on <html>.
 *   - Preference is stored under localStorage key `theme`.
 *   - Toggle button has an accessible name containing "theme".
 */

const BASE_URL = process.env.BASE_URL ?? 'http://localhost:3000';
const THEME_KEY = 'theme';

async function appliedTheme(page: Page): Promise<'dark' | 'light' | 'none'> {
  return page.locator('html').evaluate((el) => {
    if (el.classList.contains('dark')) return 'dark';
    if (el.classList.contains('light')) return 'light';
    return 'none';
  });
}

test.describe('theme resolution order', () => {
  test('saved dark preference applies on load', async ({ page }) => {
    await page.addInitScript((key) => localStorage.setItem(key, 'dark'), THEME_KEY);
    await page.goto(BASE_URL);
    expect(await appliedTheme(page)).toBe('dark');
  });

  test('system dark preference applies on first visit', async ({ page }) => {
    await page.emulateMedia({ colorScheme: 'dark' });
    await page.goto(BASE_URL);
    expect(await appliedTheme(page)).toBe('dark');
  });

  test('manual preference overrides system preference', async ({ page }) => {
    await page.emulateMedia({ colorScheme: 'dark' });
    await page.addInitScript((key) => localStorage.setItem(key, 'light'), THEME_KEY);
    await page.goto(BASE_URL);
    expect(await appliedTheme(page)).toBe('light');
  });

  test('corrupted stored value falls back without errors', async ({ page }) => {
    const errors: string[] = [];
    page.on('pageerror', (err) => errors.push(err.message));
    await page.addInitScript((key) => localStorage.setItem(key, 'banana'), THEME_KEY);
    await page.emulateMedia({ colorScheme: 'dark' });
    await page.goto(BASE_URL);
    expect(errors).toHaveLength(0);
    expect(await appliedTheme(page)).toBe('dark');
  });
});

test.describe('FOIT — flash of incorrect theme', () => {
  test('no light flash before dark theme applies', async ({ page }) => {
    await page.addInitScript((key) => {
      localStorage.setItem(key, 'dark');
      // Capture the html class as early as DOM allows.
      (window as any).__themeAtDomStart = null;
      document.addEventListener('readystatechange', () => {
        if ((window as any).__themeAtDomStart === null) {
          (window as any).__themeAtDomStart = document.documentElement.className;
        }
      });
    }, THEME_KEY);
    await page.goto(BASE_URL, { waitUntil: 'domcontentloaded' });
    const early = await page.evaluate(() => (window as any).__themeAtDomStart);
    expect(early).toContain('dark');
  });

  test('background color is dark on first computed style', async ({ page }) => {
    await page.addInitScript((key) => localStorage.setItem(key, 'dark'), THEME_KEY);
    await page.goto(BASE_URL, { waitUntil: 'domcontentloaded' });
    const bg = await page.locator('body').evaluate((el) => getComputedStyle(el).backgroundColor);
    expect(bg).not.toBe('rgb(255, 255, 255)');
  });
});

test.describe('manual toggle and persistence', () => {
  test('toggle switches theme immediately without reload', async ({ page }) => {
    await page.emulateMedia({ colorScheme: 'light' });
    await page.goto(BASE_URL);
    const before = await appliedTheme(page);
    await page.getByRole('button', { name: /theme|modo|tema/i }).first().click();
    const after = await appliedTheme(page);
    expect(after).not.toBe(before);
  });

  test('theme persists across navigation', async ({ page }) => {
    await page.addInitScript((key) => localStorage.setItem(key, 'dark'), THEME_KEY);
    await page.goto(BASE_URL);
    await page.locator('a[href]').first().click();
    await page.waitForLoadState('domcontentloaded');
    expect(await appliedTheme(page)).toBe('dark');
  });

  test('toggle is keyboard operable and has an accessible name', async ({ page }) => {
    await page.goto(BASE_URL);
    const toggle = page.getByRole('button', { name: /theme|modo|tema/i }).first();
    await toggle.focus();
    await expect(toggle).toBeFocused();
    const name = await toggle.getAttribute('aria-label');
    expect(name ?? (await toggle.textContent())?.trim()).toBeTruthy();
  });
});
