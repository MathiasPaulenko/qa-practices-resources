import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.Assert;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

public class LoginTestPOM {
    private WebDriver driver;
    private LoginPage loginPage;

    @BeforeMethod
    public void setUp() {
        driver = new ChromeDriver();
        driver.manage().window().maximize();
        // Placeholder URL — replace with your app's login page
        driver.get("https://example.com/login");
        loginPage = new LoginPage(driver);
    }

    @Test
    public void testValidLogin() {
        loginPage.login("test@test.com", "Test123!");
        Assert.assertTrue(loginPage.isDashboardVisible());
    }

    @DataProvider(name = "loginData")
    public Object[][] getLoginData() {
        return new Object[][] {
            {"test@test.com", "wrongpass", "Invalid credentials"},
            {"", "Test123!", "Email is required"},
            {"test@test.com", "", "Password is required"},
            {"invalid", "Test123!", "Please enter a valid email"},
        };
    }

    @Test(dataProvider = "loginData")
    public void testInvalidLogin(String email, String password, String expected) {
        loginPage.login(email, password);
        Assert.assertEquals(loginPage.getErrorMessage(), expected);
    }

    @AfterMethod
    public void tearDown() {
        driver.quit();
    }
}
