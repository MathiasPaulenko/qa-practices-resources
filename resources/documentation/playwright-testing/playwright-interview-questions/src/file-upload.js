await page.setInputFiles('input[type="file"]', 'testdata/upload.csv')
// Several files
await page.setInputFiles('input[type="file"]', ['file1.csv', 'file2.csv'])