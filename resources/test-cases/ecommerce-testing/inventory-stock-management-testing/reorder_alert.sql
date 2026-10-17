-- Products that crossed their reorder threshold without an alert firing.
-- Companion for https://qapractices.com/test-cases/inventory-stock-management-testing/
-- Expected: 0 rows when the reorder-alert mechanism works correctly.

SELECT sku, stock_level, reorder_threshold
FROM inventory
WHERE stock_level < reorder_threshold
  AND alert_sent = false;

-- Companion check: phantom stock — system says units exist, warehouse says none.
SELECT i.sku, i.stock_level, w.physical_count
FROM inventory i
JOIN warehouse_counts w ON w.sku = i.sku
WHERE i.stock_level > 0
  AND w.physical_count = 0;
