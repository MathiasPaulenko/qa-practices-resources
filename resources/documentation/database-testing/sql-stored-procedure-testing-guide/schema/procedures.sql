-- Sample stored procedures for SQL Server, PostgreSQL and Oracle.
-- Load this file first, then run the test files.

-- ============================================================
-- PostgreSQL: usp_order_summary
-- ============================================================
-- Run in: psql -d qa_staging -f schema/procedures.sql

CREATE SCHEMA IF NOT EXISTS qa_staging;

CREATE TABLE IF NOT EXISTS qa_staging.orders (
    id SERIAL PRIMARY KEY,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS qa_staging.order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES qa_staging.orders(id),
    amount DECIMAL(10,2) NOT NULL DEFAULT 0.00
);

CREATE OR REPLACE PROCEDURE qa_staging.usp_order_summary(p_status VARCHAR(20))
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT o.id, COALESCE(SUM(oi.amount), 0.00) AS total
    FROM qa_staging.orders o
    LEFT JOIN qa_staging.order_items oi ON oi.order_id = o.id
    WHERE o.status = p_status
    GROUP BY o.id;
END;
$$;

-- ============================================================
-- PostgreSQL: transfer_funds (with exception handling)
-- ============================================================

CREATE TABLE IF NOT EXISTS qa_staging.accounts (
    id INT PRIMARY KEY,
    balance DECIMAL(10,2) NOT NULL DEFAULT 0.00
);

CREATE OR REPLACE PROCEDURE qa_staging.transfer_funds(
    p_from INT,
    p_to INT,
    p_amount DECIMAL(10,2)
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_amount <= 0 THEN
        RAISE EXCEPTION 'Amount must be positive';
    END IF;

    UPDATE qa_staging.accounts SET balance = balance - p_amount WHERE id = p_from;
    UPDATE qa_staging.accounts SET balance = balance + p_amount WHERE id = p_to;
END;
$$;

-- ============================================================
-- SQL Server: usp_order_summary (run with sqlcmd)
-- ============================================================
/*
CREATE SCHEMA qa_staging;
GO

CREATE TABLE qa_staging.orders (
    id INT PRIMARY KEY IDENTITY(1,1),
    status NVARCHAR(20) NOT NULL DEFAULT 'pending'
);

CREATE TABLE qa_staging.order_items (
    id INT PRIMARY KEY IDENTITY(1,1),
    order_id INT NOT NULL REFERENCES qa_staging.orders(id),
    amount DECIMAL(10,2) NOT NULL DEFAULT 0.00
);

CREATE OR ALTER PROCEDURE qa_staging.usp_order_summary
    @status NVARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;
    SELECT o.id, COALESCE(SUM(oi.amount), 0.00) AS total
    FROM qa_staging.orders o
    LEFT JOIN qa_staging.order_items oi ON oi.order_id = o.id
    WHERE o.status = @status
    GROUP BY o.id;
END;
GO
*/

-- ============================================================
-- Oracle: usp_order_summary (run with sqlplus)
-- ============================================================
/*
CREATE TABLE qa_staging.orders (
    id NUMBER PRIMARY KEY,
    status VARCHAR2(20) DEFAULT 'pending' NOT NULL
);

CREATE TABLE qa_staging.order_items (
    id NUMBER PRIMARY KEY,
    order_id NUMBER NOT NULL REFERENCES qa_staging.orders(id),
    amount NUMBER(10,2) DEFAULT 0.00 NOT NULL
);

CREATE OR REPLACE PROCEDURE qa_staging.usp_order_summary(
    p_status IN VARCHAR2,
    p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_cursor FOR
    SELECT o.id, COALESCE(SUM(oi.amount), 0.00) AS total
    FROM qa_staging.orders o
    LEFT JOIN qa_staging.order_items oi ON oi.order_id = o.id
    WHERE o.status = p_status
    GROUP BY o.id;
END;
/
*/
