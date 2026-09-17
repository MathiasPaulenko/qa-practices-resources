import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.ValueSource;

import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ParameterizedTestExample {

    private final Calculator calculator = new Calculator();

    @ParameterizedTest
    @ValueSource(ints = {2, 4, 6, 8, 100})
    @DisplayName("returns true for even numbers")
    void isEven(int number) {
        assertTrue(number % 2 == 0);
    }

    @ParameterizedTest
    @CsvSource({"2, 3, 5", "-1, -2, -3", "0, 0, 0"})
    @DisplayName("adds numbers correctly")
    void addsNumbers(int a, int b, int expected) {
        assertEquals(expected, calculator.add(a, b));
    }

    @ParameterizedTest
    @MethodSource("divisionCases")
    @DisplayName("divides numbers correctly")
    void dividesNumbers(int a, int b, int expected) {
        assertEquals(expected, calculator.divide(a, b));
    }

    static Stream<org.junit.jupiter.params.provider.Arguments> divisionCases() {
        return Stream.of(
            org.junit.jupiter.params.provider.Arguments.of(10, 2, 5),
            org.junit.jupiter.params.provider.Arguments.of(9, 3, 3),
            org.junit.jupiter.params.provider.Arguments.of(1, 1, 1)
        );
    }
}
