import org.junit.jupiter.api.*;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import java.time.Duration;

public class LoginTest {
  WebDriver driver;

  @BeforeEach
  public void setUp() {
    driver = new ChromeDriver();
    driver.manage().window().maximize();
  }

  @AfterEach
  public void tearDown() {
    driver.quit();
  }

  @Test
  public void successfulLogin() {
    driver.get("https://staging.qa.local/login");
    driver.findElement(By.id("email"))
      .sendKeys("jane@qa.local");
    driver.findElement(By.id("password"))
      .sendKeys("validpass123");
    driver.findElement(By.cssSelector("[data-testid='login-button']"))
      .click();

    String currentUrl = driver.getCurrentUrl();
    Assertions.assertTrue(currentUrl.contains("/dashboard"));

    WebElement welcomeMessage = driver.findElement(
      By.xpath("//h1[contains(text(), 'Welcome')]")
    );
    Assertions.assertTrue(welcomeMessage.isDisplayed());
  }
}
