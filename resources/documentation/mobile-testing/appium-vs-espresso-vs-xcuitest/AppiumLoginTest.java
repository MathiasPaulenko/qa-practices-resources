import io.appium.java_client.AppiumBy;
import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.android.options.UiAutomator2Options;
import java.net.URI;

/**
 * Same login scenario as LoginEspressoTest.kt and LoginUITest.swift,
 * driven over HTTP by Appium Server 2.x with the UiAutomator2 driver.
 * Requires appium-java-client 9.x and a running Appium server on :4723.
 * In Appium 2.x the server base path is "/" (no /wd/hub suffix).
 */
public class AppiumLoginTest {

    public static void main(String[] args) throws Exception {
        UiAutomator2Options options = new UiAutomator2Options()
            .setDeviceName("Pixel_7")
            .setApp("/path/to/app-debug.apk")
            .setAppPackage("com.example.app")   // Placeholder: your app's package
            .setAppActivity(".MainActivity");

        AndroidDriver driver = new AndroidDriver(
            new URI("http://127.0.0.1:4723").toURL(), options);

        try {
            driver.findElement(AppiumBy.accessibilityId("email"))
                .sendKeys("qa@staging.acme.dev");
            driver.findElement(AppiumBy.accessibilityId("login")).click();
            // Assert the dashboard appears — wire your wait/assertion here.
        } finally {
            driver.quit();
        }
    }
}
