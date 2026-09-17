import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.testng.Assert.assertTrue;

public class DataProviderExample {

    // === TestNG 7.10 approach ===

    @DataProvider(name = "additionCases")
    public Object[][] additionCases() {
        return new Object[][] {
            {2, 3, 5},
            {-1, -2, -3},
            {0, 0, 0}
        };
    }

    @Test(dataProvider = "additionCases")
    public void testNgAdd(int a, int b, int expected) {
        assertEquals(a + b, expected);
    }

    // === JUnit 5.11 approach ===

    @ParameterizedTest
    @CsvSource({
        "2, 3, 5",
        "-1, -2, -3",
        "0, 0, 0"
    })
    void junit5Add(int a, int b, int expected) {
        assertEquals(expected, a + b);
    }
}
