-- tSQLt test: usp_order_summary returns correct totals
-- Run: sqlcmd -S localhost -U sa -P YourStrong123! -d qa_staging -i test/sql/test_order_summary_tsqlt.sql

EXEC tSQLt.NewTestClass 'OrderProcTests';
GO

CREATE PROCEDURE OrderProcTests.[test usp_order_summary returns correct totals]
AS
BEGIN
    -- Fake the tables so tests don't touch real data
    EXEC tSQLt.FakeTable 'qa_staging.orders';
    EXEC tSQLt.FakeTable 'qa_staging.order_items';

    -- Seed test data
    INSERT INTO qa_staging.orders (id, status) VALUES (1, 'pending'), (2, 'pending');
    INSERT INTO qa_staging.order_items (order_id, amount) VALUES (1, 100.00), (1, 50.00), (2, 230.00);

    -- Expected output
    CREATE TABLE #expected (order_id INT, total DECIMAL(10,2));
    INSERT INTO #expected VALUES (1, 150.00), (2, 230.00);

    -- Actual output
    CREATE TABLE #actual (order_id INT, total DECIMAL(10,2));
    INSERT INTO #actual
    EXEC qa_staging.usp_order_summary @status = 'pending';

    -- Assert
    EXEC tSQLt.AssertEqualsTable '#expected', '#actual';
END;
GO

CREATE PROCEDURE OrderProcTests.[test usp_order_summary returns empty set for unknown status]
AS
BEGIN
    EXEC tSQLt.FakeTable 'qa_staging.orders';
    EXEC tSQLt.FakeTable 'qa_staging.order_items';

    INSERT INTO qa_staging.orders (id, status) VALUES (1, 'pending');

    CREATE TABLE #expected (order_id INT, total DECIMAL(10,2));
    -- No rows expected

    CREATE TABLE #actual (order_id INT, total DECIMAL(10,2));
    INSERT INTO #actual
    EXEC qa_staging.usp_order_summary @status = 'nonexistent';

    EXEC tSQLt.AssertEqualsTable '#expected', '#actual';
END;
GO

-- Run tests
EXEC tSQLt.Run 'OrderProcTests';
GO
