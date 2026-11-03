# Casos de Prueba de Facturas e Historial de Facturación — Companion

Snippets de validación ejecutables para [Casos de Prueba de Facturas e Historial de Facturación](https://qapractices.com/es/test-cases/invoice-billing-history-test-cases/) en QAPractices.com.

## Contenido

- `sql/proration-validation.sql` — verifica las líneas que una subida de plan a mitad de ciclo escribe en la factura (crédito Básico −5.00, cargo Pro 15.00, neto 10.00).
- `tests/test_invoice_pdf.py` — extrae texto de un PDF de factura con pdfplumber 0.11 y asegura el número de factura y el monto de impuesto (TC002, TC015, TC023, TC025).
- `tests/invoice-download.spec.ts` — spec de Playwright 1.48 que hace clic en "Descargar PDF" en el historial y asegura el nombre sugerido del archivo (TC003, TC012).

## Uso

```bash
pip install -r requirements.txt
pytest tests/test_invoice_pdf.py          # necesita un fixture invoice.pdf en el directorio
npx playwright test tests/invoice-download.spec.ts
```

Ajusta las queries y los selectores (`[data-testid="download-invoice"]`, `/billing/history`) a tu aplicación bajo prueba.

## Recurso relacionado

- Página del recurso: https://qapractices.com/es/test-cases/invoice-billing-history-test-cases/
- Versión en inglés: https://qapractices.com/test-cases/invoice-billing-history-test-cases/
