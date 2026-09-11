// playwright.config.ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  retries: {
    production: 3,
    development: 0
  }
})