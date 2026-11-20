import static org.junit.jupiter.api.Assertions.*;
import static org.junit.jupiter.api.Assumptions.*;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * Mirrors Q4, Q5, Q6, Q7 and Q17 of the Java Testing Interview guide:
 * lifecycle annotations, @DisplayName, the assertion toolbox,
 * assumptions and exception testing.
 */
@DisplayName("Lifecycle and Assertions")
class LifecycleAndAssertionsTest {

    private static List<String> bootLog;
    private List<String> items;

    @BeforeAll
    static void setUpAll() {
        // Runs once before all tests - must be static.
        bootLog = new ArrayList<>();
        bootLog.add("expensive setup done");
    }

    @BeforeEach
    void setUp() {
        // Runs before each test - fresh state per test.
        items = new ArrayList<>();
    }

    @Test
    @DisplayName("should add item to empty list")
    void shouldAddItemToEmptyList() {
        items.add("first");

        assertAll("list state",
            () -> assertEquals(1, items.size()),
            () -> assertTrue(items.contains("first")),
            () -> assertFalse(items.isEmpty())
        );
    }

    @Test
    @DisplayName("should start empty for every test")
    void shouldStartEmptyForEveryTest() {
        // Proves @BeforeEach gives each test fresh state.
        assertTrue(items.isEmpty());
    }

    @Test
    @DisplayName("should throw on negative capacity")
    void shouldThrowOnNegativeCapacity() {
        IllegalArgumentException ex = assertThrows(
            IllegalArgumentException.class,
            () -> {
                if (items.size() < 0) {
                    throw new IllegalArgumentException("negative size");
                }
                throw new IllegalArgumentException("negative size");
            }
        );
        assertEquals("negative size", ex.getMessage());
    }

    @Test
    @DisplayName("should complete within timeout")
    void shouldCompleteWithinTimeout() {
        assertTimeout(Duration.ofSeconds(1), () -> {
            for (int i = 0; i < 100; i++) {
                items.add("item-" + i);
            }
        });
    }

    @Test
    @DisplayName("should skip when assumption fails")
    void shouldSkipWhenAssumptionFails() {
        assumeTrue("Linux".equals(System.getProperty("os.name")),
            "Linux-only test");
        // Reached only on Linux; otherwise the test reports as skipped.
        assertEquals(1, bootLog.size());
    }

    @Test
    @Disabled("demonstrates @Disabled - always skipped")
    void disabledExample() {
        fail("this line never runs");
    }

    @AfterEach
    void tearDown() {
        items = null;
    }

    @AfterAll
    static void tearDownAll() {
        bootLog = null;
    }
}
