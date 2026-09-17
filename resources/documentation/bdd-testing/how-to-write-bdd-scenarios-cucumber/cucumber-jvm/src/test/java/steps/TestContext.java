package steps;

public final class TestContext {
    private static String currentUser;

    private TestContext() {
    }

    public static void reset() {
        currentUser = null;
    }

    public static void loginAsTestUser() {
        currentUser = "jane@qapractices.com";
    }

    public static String currentUser() {
        return currentUser;
    }
}
