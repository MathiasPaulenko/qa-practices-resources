import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

@DisplayName("Calculator Tests")
class CalculatorTest {

    private Calculator calculator;

    @BeforeEach
    void setUp() {
        calculator = new Calculator();
    }

    @Test
    @DisplayName("adds two positive numbers")
    void addsTwoPositiveNumbers() {
        assertEquals(5, calculator.add(2, 3));
    }

    @Test
    @DisplayName("handles negative numbers")
    void handlesNegativeNumbers() {
        assertEquals(-3, calculator.add(-1, -2));
    }

    @Test
    @DisplayName("handles zero")
    void handlesZero() {
        assertEquals(0, calculator.add(0, 0));
    }

    @Test
    @DisplayName("divides two numbers")
    void dividesTwoNumbers() {
        assertEquals(5, calculator.divide(10, 2));
    }

    @Test
    @DisplayName("throws on division by zero")
    void throwsOnDivisionByZero() {
        assertThrows(ArithmeticException.class, () -> calculator.divide(10, 0));
    }
}
