// @playwright/test 1.x — capture a new tab via context page event
const [newPage] = await Promise.all([
  context.waitForEvent('page'),
  page.locator('#open-tab').click(),
]);
await newPage.waitForLoadState();
await newPage.close();
