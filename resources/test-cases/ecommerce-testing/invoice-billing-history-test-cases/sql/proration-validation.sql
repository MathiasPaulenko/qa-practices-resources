-- Verify proration line items for a mid-cycle upgrade (TC023 / TC025)
SELECT line_item, amount
FROM invoice_line_items
WHERE invoice_id = 'INV-2026-050'
ORDER BY line_item;

-- Expected:
-- Basic plan credit  | -5.00
-- Pro plan charge    |  15.00
