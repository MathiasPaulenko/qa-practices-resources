// cypress.config.ts (excerpt): retries per mode.
// Retry in CI where flakes live; never in interactive mode where you want
// immediate feedback.
const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    retries: {
      runMode: 2, // retry twice in CI
      openMode: 0, // no retries in `cypress open`
    },
    // GreenCart disabled video to speed up CI artifact upload.
    video: false,
  },
})
