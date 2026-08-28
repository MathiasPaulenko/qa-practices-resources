package com.cartify.tests;

import com.cartify.pages.CartPage;
import com.cartify.pages.CheckoutPage;
import com.cartify.pages.LoginPage;
import com.cartify.pages.PaymentPage;
import com.cartify.utils.RetryAnalyzer;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.testng.Assert;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;
import java.time.Duration;

/**
 * End-to-end checkout tests for Cartify.
 * Covers login → cart → checkout → payment flow.
 */
public class CheckoutTest {
    private WebDriver driver;
    private LoginPage loginPage;
    private CartPage cartPage;
    private CheckoutPage checkoutPage;
    private PaymentPage paymentPage;

    @BeforeMethod
    public void setUp() {
        ChromeOptions options = new ChromeOptions();
        options.setBrowserVersion("124");
        driver = new ChromeDriver(options);
        driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(30));
        // Placeholder: replace with your staging URL
        driver.get("https://staging.qapractices.com");
        loginPage = new LoginPage(driver);
        cartPage = new CartPage(driver);
        checkoutPage = new CheckoutPage(driver);
        paymentPage = new PaymentPage(driver);
    }

    @DataProvider(name = "checkoutData")
    public Object[][] getCheckoutData() {
        return new Object[][] {
            {"validuser@example.com", "ValidPass123!", "John Doe", "123 Main St", "Anytown", "12345",
             "4111111111111111", "12/26", "123", true},
            {"validuser@example.com", "ValidPass123!", "Jane Smith", "456 Oak Ave", "Springfield", "67890",
             "5555555555554444", "06/27", "456", true}
        };
    }

    @Test(dataProvider = "checkoutData", retryAnalyzer = RetryAnalyzer.class)
    public void testFullCheckoutFlow(String username, String password, String fullName,
            String address, String city, String zip,
            String cardNumber, String expiry, String cvv, boolean shouldSucceed) {
        // Login
        loginPage.login(username, password);

        // Verify cart has items
        Assert.assertTrue(cartPage.getCartItemCount() > 0, "Cart should have items");
        cartPage.proceedToCheckout();

        // Fill shipping address
        checkoutPage.fillShippingAddress(fullName, address, city, zip);

        // Handle payment iframe
        paymentPage.switchToPaymentIframe();
        paymentPage.enterPaymentDetails(cardNumber, expiry, cvv);
        paymentPage.clickPay();

        // Verify payment success
        Assert.assertEquals(paymentPage.isPaymentSuccessful(), shouldSucceed,
                "Payment success should match expected outcome");
    }

    @AfterMethod
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
