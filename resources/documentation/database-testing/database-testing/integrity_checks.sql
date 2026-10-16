-- Integrity checks from the guide. Each query must return 0 violations.

-- CHECK 1: no orphaned order lines (every line references an existing order)
SELECT COUNT(*) AS orphans
FROM order_lines ol
LEFT JOIN orders o ON ol.order_id = o.id
WHERE o.id IS NULL;

-- CHECK 2: order totals match line items + tax + shipping
SELECT COUNT(*) AS mismatched_totals
FROM orders o
WHERE o.total != (
  SELECT COALESCE(SUM(li.price * li.quantity), 0)
  FROM order_lines li WHERE li.order_id = o.id
) + o.tax + o.shipping;

-- CHECK 3: no duplicate user emails (UNIQUE constraint enforcement)
SELECT COUNT(*) AS duplicate_emails
FROM (
  SELECT email, COUNT(*) c FROM users
  WHERE deleted_at IS NULL
  GROUP BY email HAVING c > 1
);

-- CHECK 4: no non-positive product prices
SELECT COUNT(*) AS bad_prices
FROM products WHERE price <= 0;

-- CHECK 5: no order lines with zero or negative quantity
SELECT COUNT(*) AS bad_quantities
FROM order_lines WHERE quantity <= 0;
