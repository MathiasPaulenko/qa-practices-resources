import org.testng.annotations.Test;

public class DependencyTests {

    @Test(groups = "smoke")
    public void loginTest() {
        // Logs in and stores session state
        System.out.println("Login executed");
    }

    @Test(dependsOnMethods = "loginTest", groups = "regression")
    public void dashboardTest() {
        // Skipped if loginTest fails
        System.out.println("Dashboard verified");
    }

    @Test(dependsOnMethods = "dashboardTest", groups = "regression")
    public void logoutTest() {
        // Skipped if dashboardTest fails or is skipped
        System.out.println("Logout completed");
    }
}
