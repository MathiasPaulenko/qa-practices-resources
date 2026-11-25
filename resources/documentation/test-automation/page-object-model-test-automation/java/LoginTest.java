import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;
import static org.testng.Assert.assertEquals;

public class LoginTest {
    WebDriver driver;
    LoginPage loginPage;

    @BeforeMethod
    public void setUp() {
        driver = new ChromeDriver();
        loginPage = new LoginPage(driver);
        loginPage.navigateTo();
    }

    @Test
    public void testSuccessfulLogin() {
        DashboardPage dashboard = loginPage.login("test@qapractices.com", "Test123!");
        assertEquals(dashboard.getWelcomeMessage(), "Welcome, Test User!");
    }

    @Test
    public void testInvalidLogin() {
        loginPage.login("test@qapractices.com", "wrongpass");
        assertEquals(loginPage.getErrorMessage(), "Invalid credentials");
    }

    @AfterMethod
    public void tearDown() {
        driver.quit();
    }
}
