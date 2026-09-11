// Save state
const state = await context.storageState()
// Reuse in new context
const context = await browser.newContext({ storageState: 'state.json' })