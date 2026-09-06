package com.shop.qa;

import io.appium.java_client.AppiumBy;
import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.android.options.UiAutomator2Options;
import org.junit.jupiter.api.*;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.PointerInput;
import org.openqa.selenium.interactions.Sequence;

import java.net.MalformedURLException;
import java.net.URL;
import java.time.Duration;
import java.util.List;

/**
 * Gesture examples for Appium 2 using PointerInput and Sequence.
 * Covers swipe, scroll-to-text, and long press.
 */
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public class GestureExamplesTest {

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
    @DisplayName("Swipe gesture using PointerInput")
    void swipeToElement() {
        int height = driver.manage().window().getSize().getHeight();
        int width = driver.manage().window().getSize().getWidth();

        PointerInput finger = new PointerInput(PointerInput.Kind.TOUCH, "finger");
        Sequence swipe = new Sequence(finger, 0);

        swipe.addAction(finger.createPointerMove(
            Duration.ofMillis(0),
            PointerInput.Origin.viewport(),
            width / 2 + 200, height / 2
        ));
        swipe.addAction(finger.createPointerDown(PointerInput.MouseButton.LEFT.asArg()));
        swipe.addAction(finger.createPointerMove(
            Duration.ofMillis(800),
            PointerInput.Origin.viewport(),
            width / 2 - 200, height / 2
        ));
        swipe.addAction(finger.createPointerUp(PointerInput.MouseButton.LEFT.asArg()));

        driver.perform(List.of(swipe));
    }

    @Test
    @DisplayName("Scroll to text using Android UIAutomator")
    void scrollToText() {
        WebElement element = driver.findElement(
            AppiumBy.androidUIAutomator(
                "new UiScrollable(new UiSelector().scrollable(true))" +
                ".scrollIntoView(new UiSelector().text(\"Settings\"))"
            )
        );
        element.click();
    }

    @Test
    @DisplayName("Long press gesture using PointerInput")
    void longPressElement() {
        WebElement element = driver.findElement(
            AppiumBy.accessibilityId("long-press-target")
        );

        PointerInput finger = new PointerInput(PointerInput.Kind.TOUCH, "finger");
        Sequence longPress = new Sequence(finger, 0);

        longPress.addAction(finger.createPointerMove(
            Duration.ofMillis(0),
            PointerInput.Origin.viewport(),
            element.getLocation().getX() + element.getSize().getWidth() / 2,
            element.getLocation().getY() + element.getSize().getHeight() / 2
        ));
        longPress.addAction(finger.createPointerDown(PointerInput.MouseButton.LEFT.asArg()));
        longPress.addAction(finger.createPointerMove(
            Duration.ofMillis(2000),
            PointerInput.Origin.viewport(),
            element.getLocation().getX() + element.getSize().getWidth() / 2,
            element.getLocation().getY() + element.getSize().getHeight() / 2
        ));
        longPress.addAction(finger.createPointerUp(PointerInput.MouseButton.LEFT.asArg()));

        driver.perform(List.of(longPress));
    }
}
