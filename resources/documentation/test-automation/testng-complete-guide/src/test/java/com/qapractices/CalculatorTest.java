package com.qapractices;

import org.testng.annotations.*;
import org.testng.Assert;

public class CalculatorTest {
    private Calculator calculator;

    @BeforeClass(alwaysRun = true)
    public void setUp() {
        calculator = new Calculator();
    }

    @AfterClass(alwaysRun = true)
    public void tearDown() {
        calculator = null;
    }

    @Test(groups = {"smoke", "regression"}, testName = "Add two positive numbers")
    public void testAdd() {
        int result = calculator.add(5, 3);
        Assert.assertEquals(result, 8, "5 + 3 should equal 8");
    }

    @Test(groups = {"regression"}, testName = "Subtract two numbers")
    public void testSubtract() {
        int result = calculator.subtract(10, 4);
        Assert.assertEquals(result, 6, "10 - 4 should equal 6");
    }

    @Test(groups = {"smoke", "regression"}, testName = "Divide by zero throws exception")
    public void testDivideByZero() {
        Assert.assertThrows(
            ArithmeticException.class,
            () -> calculator.divide(10, 0)
        );
    }
}
