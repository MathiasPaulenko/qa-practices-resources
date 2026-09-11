const [download] = await Promise.all([
  page.waitForEvent('download'),
  page.click('#download-button')
])
const path = await download.path()
const filename = download.suggestedFilename()
await download.saveAs('downloads/' + filename)