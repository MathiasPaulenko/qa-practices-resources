package com.cartify.tests;

import com.cartify.pages.LoginPage;
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
 * Login tests for Cartify checkout.
 * Uses Selenium Manager for driver management (Selenium 4.6+).
 */
public class LoginTest {
    private WebDriver driver;
    private LoginPage loginPage;

    @BeforeMethod
    public void setUp() {
        ChromeOptions options = new ChromeOptions();
        options.setBrowserVersion("124");
        driver = new ChromeDriver(options);
        driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(30));
        // Placeholder: replace with your staging URL
        driver.get("https://staging.qapractices.com/login");
        loginPage = new LoginPage(driver);
    }

    @DataProvider(name = "loginData")
    public Object[][] getLoginData() {
        return new Object[][] {
            {"validuser@example.com", "ValidPass123!", true},
            {"invaliduser@example.com", "WrongPass456", false},
            {"", "", false}
        };
    }

    @Test(dataProvider = "loginData", retryAnalyzer = RetryAnalyzer.class)
    public void testLogin(String username, String password, boolean shouldSucceed) {
        loginPage.login(username, password);
        if (shouldSucceed) {
            Assert.assertFalse(loginPage.isLoginButtonDisplayed(),
                    "Login button should not be visible after successful login");
        } else {
            Assert.assertTrue(loginPage.getErrorMessage().contains("Invalid"),
                    "Error message should be displayed for failed login");
        }
    }

    @AfterMethod
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
