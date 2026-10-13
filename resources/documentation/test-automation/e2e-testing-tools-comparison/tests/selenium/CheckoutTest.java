// Selenium 4.25 with Java 21 — checkout flow smoke test
// Run: mvn test -Dtest=CheckoutTest

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

import static org.junit.jupiter.api.Assertions.assertTrue;

class CheckoutTest {

    private WebDriver driver;
    private WebDriverWait wait;

    @BeforeEach
    void setUp() {
        driver = new ChromeDriver();
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    @AfterEach
    void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }

    @Test
    void completesCheckout() {
        driver.get("https://staging.lumapay.com/checkout");
        wait.until(ExpectedConditions.elementToBeClickable(By.id("pay"))).click();
        wait.until(ExpectedConditions.visibilityOfElementLocated(
                By.xpath("//*[contains(text(),'Payment confirmed')]")));
        assertTrue(driver.getPageSource().contains("Payment confirmed"));
    }

    @Test
    void handlesDeclinedPayment() {
        driver.get("https://staging.lumapay.com/checkout?scenario=declined");
        wait.until(ExpectedConditions.elementToBeClickable(By.id("pay"))).click();
        wait.until(ExpectedConditions.visibilityOfElementLocated(
                By.xpath("//*[contains(text(),'Payment failed')]")));
        assertTrue(driver.getPageSource().contains("Payment failed"));
    }
}
