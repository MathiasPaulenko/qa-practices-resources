package com.qapractices.appium;

import io.appium.java_client.AppiumBy;
import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.android.Connection;
import io.appium.java_client.android.nativekey.NetworkConnectionSetting;
import io.appium.java_client.android.options.UiAutomator2Options;
import io.appium.java_client.ios.IOSDriver;
import io.appium.java_client.ios.options.XCUITestOptions;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.ScreenOrientation;
import org.openqa.selenium.interactions.PointerInput;
import org.openqa.selenium.interactions.Sequence;
import org.openqa.selenium.remote.RemoteWebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.io.File;
import java.net.URL;
import java.time.Duration;
import java.util.List;
import java.util.Map;

/**
 * Compilable companion for the Appium Commands Cheat Sheet on QAPractices.
 * Each method mirrors a section of the resource; snippets assume a live
 * session against a running Appium 2.x server.
 */
public class AppiumCommandsExamples {

    // ── Driver Setup ────────────────────────────────────────────────

    AndroidDriver androidDriver() throws Exception {
        UiAutomator2Options options = new UiAutomator2Options()
                .setDeviceName("emulator-5554")
                .setApp("/path/to/app.apk")
                .setAppPackage("com.example.app")
                .setAppActivity(".MainActivity")
                .setNoReset(false);

        return new AndroidDriver(new URL("http://localhost:4723"), options);
    }

    IOSDriver iosDriver() throws Exception {
        XCUITestOptions iosOptions = new XCUITestOptions()
                .setDeviceName("iPhone 15")
                .setPlatformVersion("17.0")
                .setBundleId("com.example.app")
                .setUdid("<device-udid>");

        return new IOSDriver(new URL("http://localhost:4723"), iosOptions);
    }

    // ── Locators ────────────────────────────────────────────────────

    void locators(AndroidDriver driver) {
        driver.findElement(AppiumBy.accessibilityId("LoginButton"));
        driver.findElement(AppiumBy.id("com.example.app:id/button"));
        driver.findElement(AppiumBy.className("android.widget.Button"));
        driver.findElement(AppiumBy.xpath("//android.widget.Button[@text='Login']"));

        driver.findElement(AppiumBy.androidUIAutomator(
                "new UiSelector().text(\"Login\")"));
        driver.findElement(AppiumBy.androidUIAutomator(
                "new UiSelector().resourceId(\"com.example:id/email\")"));
    }

    void iosLocators(IOSDriver driver) {
        driver.findElement(AppiumBy.iOSClassChain(
                "**/XCUIElementTypeButton[`label == 'Login'`]"));
        driver.findElement(AppiumBy.iOSNsPredicateString(
                "label == 'Login' AND enabled == true"));
    }

    // ── App management (Appium 2.x lifecycle) ───────────────────────

    void appManagement(AndroidDriver driver) {
        driver.installApp("/path/to/app.apk");
        driver.removeApp("com.example.app");
        boolean installed = driver.isAppInstalled("com.example.app");

        driver.activateApp("com.example.app");
        driver.terminateApp("com.example.app");
        driver.runAppInBackground(Duration.ofSeconds(10));

        Map<String, String> appStrings = driver.getAppStringMap();
    }

    // ── UiAutomator2 mobile: gestures ───────────────────────────────

    void gestures(AndroidDriver driver, RemoteWebElement element, RemoteWebElement sourceElement) {
        // Tap on coordinates — clickGesture, NOT mobile: tap
        ((JavascriptExecutor) driver).executeScript("mobile: clickGesture", Map.of(
                "x", 200, "y", 400));

        // Long press — duration is required
        ((JavascriptExecutor) driver).executeScript("mobile: longClickGesture", Map.of(
                "elementId", element.getId(), "duration", 2000));

        // Swipe — direction is REQUIRED
        ((JavascriptExecutor) driver).executeScript("mobile: swipeGesture", Map.of(
                "left", 100, "top", 500, "width", 800, "height", 200,
                "direction", "up", "percent", 0.75));

        // Scroll — direction is also required
        ((JavascriptExecutor) driver).executeScript("mobile: scrollGesture", Map.of(
                "left", 200, "top", 800, "width", 400, "height", 600,
                "direction", "down", "percent", 0.5));

        // Drag an element to coordinates
        ((JavascriptExecutor) driver).executeScript("mobile: dragGesture", Map.of(
                "elementId", sourceElement.getId(), "endX", 300, "endY", 600));

        // Pinch in / pinch out
        ((JavascriptExecutor) driver).executeScript("mobile: pinchCloseGesture", Map.of(
                "left", 200, "top", 400, "width", 400, "height", 400, "percent", 0.5));
        ((JavascriptExecutor) driver).executeScript("mobile: pinchOpenGesture", Map.of(
                "left", 200, "top", 400, "width", 400, "height", 400, "percent", 0.5));
    }

    // ── W3C Actions ─────────────────────────────────────────────────

    void w3cSwipe(AndroidDriver driver) {
        PointerInput finger = new PointerInput(PointerInput.Kind.TOUCH, "finger");
        Sequence swipe = new Sequence(finger, 0);

        swipe.addAction(finger.createPointerMove(Duration.ofMillis(0),
                PointerInput.Origin.viewport(), 500, 1000));
        swipe.addAction(finger.createPointerDown(PointerInput.MouseButton.LEFT.asArg()));
        swipe.addAction(finger.createPointerMove(Duration.ofMillis(500),
                PointerInput.Origin.viewport(), 500, 300));
        swipe.addAction(finger.createPointerUp(PointerInput.MouseButton.LEFT.asArg()));

        driver.perform(List.of(swipe));
    }

    // ── Device commands ─────────────────────────────────────────────

    void deviceCommands(AndroidDriver driver) {
        driver.getOrientation();
        driver.rotate(ScreenOrientation.LANDSCAPE);

        File screenshot = driver.getScreenshotAs(OutputType.FILE);

        driver.setClipboardText("text");
        String text = driver.getClipboardText();

        driver.hideKeyboard();
        boolean kbShown = driver.isKeyboardShown();

        driver.openNotifications();

        driver.setConnection(
                new NetworkConnectionSetting(false, true, false));
        Connection connection = driver.getConnection();
    }

    // ── Device information ──────────────────────────────────────────

    void deviceInfo(AndroidDriver driver) {
        driver.getDeviceTime();
        driver.getBatteryInfo();
        driver.getSystemBars();
        driver.getDisplayDensity();
        driver.getPerformanceData("com.example.app", "cpuinfo", 5);
    }

    // ── Waits ───────────────────────────────────────────────────────

    void waits(AndroidDriver driver) {
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(2));

        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        wait.until(ExpectedConditions.presenceOfElementLocated(
                AppiumBy.id("com.example:id/button")));
        wait.until(ExpectedConditions.elementToBeClickable(
                AppiumBy.accessibilityId("Login")));
    }
}
