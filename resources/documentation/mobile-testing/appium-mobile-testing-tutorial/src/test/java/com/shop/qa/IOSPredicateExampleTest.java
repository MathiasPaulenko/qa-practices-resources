package com.shop.qa;

import io.appium.java_client.AppiumBy;
import io.appium.java_client.ios.IOSDriver;
import io.appium.java_client.ios.options.XCUITestOptions;
import org.junit.jupiter.api.*;
import org.openqa.selenium.WebElement;

import java.net.MalformedURLException;
import java.net.URL;

/**
 * iOS Predicate String locator example using XCUITest driver.
 * Faster and more stable than XPath for complex iOS queries.
 */
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public class IOSPredicateExampleTest {

    private IOSDriver driver;

    @BeforeAll
    void setUp() throws MalformedURLException {
        XCUITestOptions options = new XCUITestOptions()
            .setDeviceName("iPhone 15")
            .setPlatformName("iOS")
            .setPlatformVersion("17.5")
            .setApp("/path/to/app.app")
            .setBundleId("com.shop.qa.ios")
            .setAutoAcceptAlerts(true)
            .setNoReset(true);

        driver = new IOSDriver(
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
    @DisplayName("Find iOS element with predicate string")
    void findIosElementWithPredicate() {
        WebElement submitButton = driver.findElement(
            AppiumBy.iOSNsPredicateString("type == 'XCUIElementTypeButton' AND label == 'Submit'")
        );
        submitButton.click();
    }
}
