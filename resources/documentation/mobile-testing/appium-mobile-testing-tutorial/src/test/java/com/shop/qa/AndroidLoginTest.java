package com.shop.qa;

import io.appium.java_client.AppiumBy;
import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.android.options.UiAutomator2Options;
import org.junit.jupiter.api.*;
import org.openqa.selenium.WebElement;

import java.net.MalformedURLException;
import java.net.URL;

/**
 * Android login test using Appium 2 with UiAutomator2 driver.
 * Uses accessibilityId locators and explicit waits.
 */
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public class AndroidLoginTest {

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
    @DisplayName("User can log in with valid credentials")
    void successfulLogin() {
        WebElement emailField = driver.findElement(
            AppiumBy.accessibilityId("email-input")
        );
        emailField.sendKeys("qa-tester@qa.local");

        WebElement passwordField = driver.findElement(
            AppiumBy.accessibilityId("password-input")
        );
        passwordField.sendKeys("secretpassword");

        WebElement loginButton = driver.findElement(
            AppiumBy.accessibilityId("login-button")
        );
        loginButton.click();

        WebElement dashboard = driver.findElement(
            AppiumBy.id("com.shop.qa:id/dashboard_container")
        );
        Assertions.assertTrue(dashboard.isDisplayed());
    }
}
