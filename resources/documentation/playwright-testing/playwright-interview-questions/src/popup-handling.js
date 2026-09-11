const [newPage] = await Promise.all([
  page.waitForEvent('popup'),
  page.click('a[target="_blank"]')
])
await newPage.waitForLoadState()
await newPage.getByText('New Page Content').click()