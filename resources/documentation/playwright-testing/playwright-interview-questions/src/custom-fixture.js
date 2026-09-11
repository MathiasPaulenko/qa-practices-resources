import { test as base } from '@playwright/test'

export const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    await page.goto('/login')
    await page.fill('#email', 'user@test.com')
    await page.click('button[type=submit]')
    await use(page)
  }
})