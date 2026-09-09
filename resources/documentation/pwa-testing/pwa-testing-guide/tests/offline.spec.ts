import { test, expect } from '@playwright/test'

test('app shell loads when offline', async ({ page, context }) => {
  await page.goto('/')
  await page.waitForLoadState('networkidle')

  const sw = await context.waitForEvent('serviceworker')
  expect(sw.url()).toContain('sw.js')

  await context.setOffline(true)
  await page.reload()

  await expect(page.getByTestId('app-shell')).toBeVisible()
})

test('offline fallback page renders', async ({ page, context }) => {
  await page.goto('/')
  await page.waitForLoadState('networkidle')

  await context.waitForEvent('serviceworker')
  await context.setOffline(true)

  await page.goto('/nonexistent-page', { waitUntil: 'domcontentloaded' })

  // The NetworkFirst strategy should fall back to /offline.html
  await expect(page.getByTestId('offline-banner')).toBeVisible()
})

test('cache updates when network returns', async ({ page, context }) => {
  await page.goto('/')
  await page.waitForLoadState('networkidle')

  await context.waitForEvent('serviceworker')
  await context.setOffline(true)
  await page.reload()
  await expect(page.getByTestId('app-shell')).toBeVisible()

  await context.setOffline(false)
  await page.reload()
  await expect(page.getByTestId('app-shell')).toBeVisible()
  await expect(page.getByTestId('online-indicator')).toBeVisible()
})
