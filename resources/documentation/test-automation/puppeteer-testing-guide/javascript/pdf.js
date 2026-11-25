describe('PDF generation', () => {
  it('generates PDF from page', async () => {
    await page.goto('https://staging.myapp.com/report', {
      waitUntil: 'networkidle0',
    });

    await page.pdf({
      path: 'reports/report.pdf',
      format: 'A4',
      printBackground: true,
      margin: {
        top: '20px',
        bottom: '20px',
        left: '20px',
        right: '20px',
      },
    });
  });
});
