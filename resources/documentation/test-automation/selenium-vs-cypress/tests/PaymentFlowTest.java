import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

import java.time.Duration;

/**
 * Selenium 4.52 + TestNG: completes a 3-D Secure payment that opens a
 * second window on a different domain — the flow Cypress cannot drive
 * natively. Replace checkout.finova.example / secure-provider.example
 * (RFC 2606 placeholders) with your staging URLs.
 */
public class PaymentFlowTest {
    private WebDriver driver;

    @BeforeMethod
    public void setUp() {
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless=new", "--window-size=1920,1080");
        options.setBrowserVersion("157");
        driver = new ChromeDriver(options);
    }

    @Test
    public void shouldComplete3DSecurePayment() {
        driver.get("https://checkout.finova.example"); // Placeholder: replace with staging URL
        driver.findElement(By.cssSelector("[data-testid='card-number']"))
              .sendKeys("4111111111111111");
        driver.findElement(By.cssSelector("[data-testid='pay-button']")).click();

        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));
        wait.until(ExpectedConditions.numberOfWindowsToBe(2));

        String original = driver.getWindowHandle();
        for (String handle : driver.getWindowHandles()) {
            if (!handle.equals(original)) driver.switchTo().window(handle);
        }

        wait.until(ExpectedConditions.urlContains("secure-provider.example"));
        driver.findElement(By.id("challenge-otp")).sendKeys("123456");
        driver.findElement(By.id("submit-otp")).click();

        driver.close();
        driver.switchTo().window(original);

        wait.until(ExpectedConditions.textToBe(
            By.cssSelector("[data-testid='payment-status']"), "Approved"));
    }

    @AfterMethod
    public void tearDown() { driver.quit(); }
}
