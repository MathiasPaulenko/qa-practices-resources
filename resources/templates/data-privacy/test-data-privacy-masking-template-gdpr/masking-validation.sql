-- masking-validation.sql
-- Validation gate for the test-data masking pipeline (PostgreSQL).
-- Run after the masking job, before loading to the test environment.
-- Every query must return 0; any count > 0 fails the gate.

-- TD-001: no real emails (all masked emails end in @example.test)
SELECT COUNT(*) AS suspicious_emails
FROM customers
WHERE email IS NOT NULL
  AND email NOT LIKE '%@example.test';

-- TD-002: no raw SSNs left (must be masked 'XXX-XX-XXXX' or NULL)
SELECT COUNT(*) AS unmasked_ssns
FROM customers
WHERE ssn ~ '^[0-9]{3}-[0-9]{2}-[0-9]{4}$';

-- TD-003: no real card numbers (must be tokenized 'tok_%' or NULL)
SELECT COUNT(*) AS unmasked_cards
FROM customers
WHERE card_number ~ '^[0-9]{13,19}$';

-- TD-004: no real phone numbers (masked phones use the 555 prefix)
SELECT COUNT(*) AS suspicious_phones
FROM customers
WHERE phone IS NOT NULL
  AND phone !~ '^\+[0-9]+-555-';

-- TD-005: no public IPs (masked IPs live in private ranges)
SELECT COUNT(*) AS public_ips
FROM customers
WHERE last_login_ip IS NOT NULL
  AND last_login_ip !~ '^(10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.)';

-- TD-006: referential integrity — every orders.customer_id must exist
SELECT COUNT(*) AS orphan_orders
FROM orders o
LEFT JOIN customers c ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL;

-- TD-007: format preserved — emails still parse as emails
SELECT COUNT(*) AS malformed_emails
FROM customers
WHERE email IS NOT NULL
  AND email !~ '^[^@\s]+@[^@\s]+\.[a-z]+$';
