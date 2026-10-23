-- sp_CreateOrder — MySQL 8.x dialect.
-- Creates an order, decrements stock and writes an audit entry atomically.
-- Run after seed.sql.

DELIMITER //

DROP PROCEDURE IF EXISTS sp_CreateOrder //

CREATE PROCEDURE sp_CreateOrder(
  IN p_customer_id INT,
  IN p_product_id  VARCHAR(64),
  IN p_quantity    INT
)
BEGIN
  DECLARE v_order_id INT;
  DECLARE v_unit_price DECIMAL(10,2);
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    ROLLBACK;
    RESIGNAL;
  END;

  -- Validation happens before any write.
  IF p_quantity IS NULL OR p_quantity <= 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'quantity must be greater than zero';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM customers WHERE customer_id = p_customer_id) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'customer not found';
  END IF;

  SELECT price INTO v_unit_price FROM products WHERE product_id = p_product_id;

  IF v_unit_price IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'product not found';
  END IF;

  START TRANSACTION;

    UPDATE inventory
       SET stock_count = stock_count - p_quantity
     WHERE product_id = p_product_id
       AND stock_count >= p_quantity;

    IF ROW_COUNT() = 0 THEN
      SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'insufficient stock';
    END IF;

    INSERT INTO orders (customer_id, status) VALUES (p_customer_id, 'pending');
    SET v_order_id = LAST_INSERT_ID();

    INSERT INTO order_items (order_id, product_id, quantity, unit_price)
    VALUES (v_order_id, p_product_id, p_quantity, v_unit_price);

    INSERT INTO order_audit (order_id, action) VALUES (v_order_id, 'created');

  COMMIT;
END //

DELIMITER ;
