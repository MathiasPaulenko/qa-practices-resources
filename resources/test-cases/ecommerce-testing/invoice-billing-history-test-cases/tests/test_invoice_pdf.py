"""Invoice PDF content checks with pdfplumber 0.11 (TC003, TC017, TC029, TC031)."""
import pdfplumber

INVOICE_PATH = "invoice.pdf"


def extract_text(path: str) -> str:
    with pdfplumber.open(path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def test_invoice_pdf_contains_amount():
    text = extract_text(INVOICE_PATH)
    assert "INV-2026-050" in text
    assert "$3.17" in text


def test_invoice_pdf_shows_payment_status():
    text = extract_text(INVOICE_PATH).lower()
    assert "paid" in text or "unpaid" in text or "failed" in text
