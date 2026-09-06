package com.shop.qa;

import io.appium.java_client.AppiumBy;
import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.android.options.UiAutomator2Options;
import org.junit.jupiter.api.*;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.net.MalformedURLException;
import java.net.URL;
import java.time.Duration;

/**
 * Explicit wait examples replacing Thread.sleep().
 * Uses WebDriverWait with ExpectedConditions.
 */
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public class ExplicitWaitTest {

    private AndroidDriver driver;

    @BeforeAll
    void setUp() throws MalformedURLException {
        UiAutomator2Options options = new UiAutomator2Options()
            .setDeviceName("Pixel_7_API_34")
            .setApp("/path/to/app.apk")
            .setAppPackage("com.shop.qa")
            .setAppActivity("com.shop.qa.MainActivity")
            .setNoReset(true);

        driver = new AndroidDriver(
            new URL("http://localhost:4723"),
            options
        );
    }

    @AfterAll
    void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }

    @Test
    @DisplayName("Login with explicit waits instead of Thread.sleep")
    void loginWithExplicitWait() {
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

        WebElement emailField = wait.until(
            ExpectedConditions.visibilityOfElementLocated(
                AppiumBy.accessibilityId("email-input")
            )
        );
        emailField.sendKeys("qa-tester@qa.local");

        WebElement loginButton = wait.until(
            ExpectedConditions.elementToBeClickable(
                AppiumBy.accessibilityId("login-button")
            )
        );
        loginButton.click();
    }
}
