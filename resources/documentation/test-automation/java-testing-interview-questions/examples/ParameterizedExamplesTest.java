import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.stream.Stream;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.ValueSource;

/**
 * Mirrors Q8 of the Java Testing Interview guide:
 * @ParameterizedTest with @ValueSource, @CsvSource and @MethodSource.
 */
class ParameterizedExamplesTest {

    record User(String name, String email) {
        boolean hasValidEmail() {
            return email != null && email.contains("@") && email.contains(".");
        }
    }

    @ParameterizedTest
    @ValueSource(ints = {1, 2, 3, 4, 5})
    @DisplayName("positive numbers pass the check")
    void positiveNumbers(int number) {
        assertTrue(number > 0);
    }

    @ParameterizedTest
    @ValueSource(strings = {"", "  ", "\t"})
    @DisplayName("blank strings are detected")
    void blankStrings(String input) {
        assertTrue(input.isBlank());
    }

    @ParameterizedTest
    @CsvSource({
        "1, 1, 2",
        "2, 3, 5",
        "-1, 1, 0",
        "0, 0, 0"
    })
    @DisplayName("addition table")
    void addition(int a, int b, int expected) {
        assertEquals(expected, Integer.sum(a, b));
    }

    @ParameterizedTest
    @MethodSource("userProvider")
    @DisplayName("email validation across users")
    void emailValidation(User user, boolean expected) {
        assertEquals(expected, user.hasValidEmail());
    }

    static Stream<Arguments> userProvider() {
        return Stream.of(
            Arguments.of(new User("Alice", "alice@test.com"), true),
            Arguments.of(new User("Bob", "bob.company"), false),
            Arguments.of(new User("", "no-name@test.com"), true)
        );
    }
}
