import { test, expect } from '@playwright/test'

test('install prompt is eligible', async ({ page }) => {
  await page.goto('/')
  await page.waitForLoadState('networkidle')

  const beforeInstall = await page.evaluate(() => {
    return new Promise((resolve) => {
      window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault()
        resolve(true)
      })
      setTimeout(() => resolve(false), 5000)
    })
  })
  expect(beforeInstall).toBe(true)
})

test('manifest is valid and served with correct MIME type', async ({ page }) => {
  const response = await page.goto('/manifest.json')
  expect(response?.status()).toBe(200)
  const contentType = response?.headers()['content-type'] || ''
  expect(contentType).toContain('application/manifest+json')

  const manifest = await response?.json()
  expect(manifest.name).toBeTruthy()
  expect(manifest.short_name).toBeTruthy()
  expect(manifest.start_url).toBeTruthy()
  expect(manifest.display).toMatch(/standalone|fullscreen|minimal-ui|window-controls-overlay/)
  expect(manifest.icons).toBeDefined()
  const has512 = manifest.icons.some(
    (i: { sizes: string }) => i.sizes === '512x512'
  )
  expect(has512).toBe(true)
})

test('service worker is activated and running', async ({ page, context }) => {
  await page.goto('/')
  await page.waitForLoadState('networkidle')

  const sw = await context.waitForEvent('serviceworker')
  expect(sw.url()).toContain('sw.js')
})
