# Invoice and Billing History Test Cases — Companion

Runnable validation snippets for [Invoice and Billing History Test Cases](https://qapractices.com/test-cases/invoice-billing-history-test-cases/) on QAPractices.com.

## Contents

- `sql/proration-validation.sql` — verifies the line items a mid-cycle plan upgrade writes on the invoice (Basic credit −$5.00, Pro charge $15.00, net $10.00).
- `tests/test_invoice_pdf.py` — extracts text from a generated invoice PDF with pdfplumber 0.11 and asserts invoice number and tax amount (TC002, TC015, TC023, TC025).
- `tests/invoice-download.spec.ts` — Playwright 1.48 spec that clicks "Download PDF" in billing history and asserts the suggested filename (TC003, TC012).

## Usage

```bash
pip install -r requirements.txt
pytest tests/test_invoice_pdf.py          # needs an invoice.pdf fixture in the working dir
npx playwright test tests/invoice-download.spec.ts
```

Adjust the queries and selectors (`[data-testid="download-invoice"]`, `/billing/history`) to your app under test.

## Related resource

- Resource page: https://qapractices.com/test-cases/invoice-billing-history-test-cases/
- Spanish version: https://qapractices.com/es/test-cases/invoice-billing-history-test-cases/
