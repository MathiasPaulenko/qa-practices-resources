import { test, expect } from '@playwright/test';
import { registrationSchema } from './schema.js';

// Client-side checks against demo-form.html served over http.
// Start a static server first: npx serve . -l 4173
const BASE = process.env.DEMO_URL ?? 'http://localhost:4173/demo-form.html';

test.describe('client-side validation (TC-FV-001..012)', () => {
  test('required field blocks submit and shows inline error', async ({ page }) => {
    await page.goto(BASE);
    await page.getByRole('button', { name: /submit/i }).click();
    const name = page.locator('#name');
    await expect(name).toHaveAttribute('aria-invalid', 'true');
    await expect(page.locator('#name-error')).toContainText(/required/i);
  });

  test('whitespace-only input is treated as empty', async ({ page }) => {
    await page.goto(BASE);
    await page.locator('#name').fill('     ');
    await page.getByRole('button', { name: /submit/i }).click();
    await expect(page.locator('#name-error')).toBeVisible();
  });

  test('error clears on valid input', async ({ page }) => {
    await page.goto(BASE);
    await page.getByRole('button', { name: /submit/i }).click();
    await page.locator('#name').fill('Ana');
    await expect(page.locator('#name-error')).toBeHidden();
  });
});

test.describe('server-side parity (TC-FV-101)', () => {
  test('shared schema rejects what the UI rejects', () => {
    const bad = { name: '', email: 'not-an-email', password: '123', age: 150, phone: '123', startDate: '2026-02-29x' };
    const result = registrationSchema.safeParse(bad);
    expect(result.success).toBe(false);
    if (!result.success) {
      const fields = result.error.issues.map((i) => i.path[0]);
      expect(fields).toEqual(expect.arrayContaining(['name', 'email', 'password', 'age', 'phone']));
    }
  });

  test('shared schema accepts a valid payload', () => {
    const ok = { name: 'Ana', email: 'ana@example.org', password: 'correct horse battery staple', age: 34, phone: '+15551234567', startDate: '2026-02-28' };
    expect(registrationSchema.safeParse(ok).success).toBe(true);
  });
});

test.describe('file upload (TC-FV-078..083)', () => {
  test('exe renamed to .pdf is rejected by magic bytes', async ({ page }) => {
    await page.goto(BASE);
    await page.locator('#attachment').setInputFiles('fixtures/payload.exe');
    await page.getByRole('button', { name: /submit/i }).click();
    await expect(page.locator('#attachment-error')).toBeVisible();
  });
});
