-- Clean seed data: every integrity check should report 0 violations.

INSERT INTO users (id, email, name) VALUES
  (1, 'ana@urbanthreads.com', 'Ana Lopez'),
  (2, 'marco@urbanthreads.com', 'Marco Ruiz');

INSERT INTO products (id, name, price) VALUES
  (1, 'Canvas jacket', 89.99),
  (2, 'Denim jeans', 59.50),
  (3, 'Summer sneakers', 120.00);

-- Order 1: 2 jackets + 1 jeans -> 239.48 items, tax 21.55, shipping 5.00
INSERT INTO orders (id, user_id, total, tax, shipping) VALUES
  (1, 1, 266.03, 21.55, 5.00);

INSERT INTO order_lines (id, order_id, product_id, quantity, price) VALUES
  (1, 1, 1, 2, 89.99),
  (2, 1, 2, 1, 59.50);
