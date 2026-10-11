package qa;

import static org.junit.jupiter.api.Assertions.*;

import java.nio.file.Paths;
import java.time.Duration;
import java.util.List;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.SearchContext;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.FluentWait;
import org.openqa.selenium.support.ui.Wait;
import org.openqa.selenium.support.ui.WebDriverWait;

/**
 * Runnable examples from "How to Handle Dynamic Web Elements in Selenium"
 * (Selenium 4.25+, Chrome). Runs against local HTML fixtures — no network
 * needed. ChromeDriver must be on PATH or managed via Selenium Manager.
 */
class DynamicElementsTest {

  private WebDriver driver;
  private WebDriverWait wait;

  @BeforeEach
  void setUp() {
    ChromeOptions options = new ChromeOptions();
    options.addArguments("--headless=new");
    driver = new ChromeDriver(options);
    wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  }

  @AfterEach
  void tearDown() {
    driver.quit();
  }

  private static String fixture(String name) {
    return Paths.get("..", "fixtures", name).toUri().toString();
  }

  @Test
  void dynamicId_locateByStableTestIdAndWaitClickable() {
    driver.get(fixture("dynamic-page.html"));

    // The button ID is regenerated on every load — data-testid is stable.
    WebElement button = wait.until(ExpectedConditions.elementToBeClickable(
        By.cssSelector("[data-testid='save-button']")));

    // Fallback without data-testid: match the stable ID prefix.
    WebElement fallback = driver.findElement(
        By.cssSelector("button[id^='btn_']"));

    assertTrue(button.isDisplayed());
    assertTrue(fallback.isDisplayed());
  }

  @Test
  void ajaxContent_waitForSpinnerToDisappearThenResults() {
    driver.get(fixture("dynamic-page.html"));

    wait.until(ExpectedConditions.invisibilityOfElementLocated(
        By.id("spinner")));
    wait.until(ExpectedConditions.numberOfElementsToBeMoreThan(
        By.cssSelector(".search-result"), 0));

    List<WebElement> results =
        driver.findElements(By.cssSelector(".search-result"));
    assertEquals(5, results.size());
  }

  @Test
  void dynamicDropdown_clickThenWaitForOptions() {
    driver.get(fixture("dynamic-page.html"));

    driver.findElement(By.id("dropdown-trigger")).click();
    wait.until(ExpectedConditions.visibilityOfElementLocated(
        By.cssSelector(".dropdown-option")));

    List<WebElement> options =
        driver.findElements(By.cssSelector(".dropdown-option"));
    options.stream()
        .filter(o -> o.getText().equals("Desired Option"))
        .findFirst()
        .orElseThrow()
        .click();
  }

  @Test
  void shadowDom_nativeGetShadowRoot() {
    driver.get(fixture("dynamic-page.html"));

    // Selenium 4 native shadow DOM support.
    WebElement host = driver.findElement(By.cssSelector("#shadow-host"));
    SearchContext shadowRoot = host.getShadowRoot();

    WebElement shadowButton =
        shadowRoot.findElement(By.cssSelector("#shadow-button"));
    assertTrue(shadowButton.isDisplayed());
  }

  @Test
  void customWait_waitForElementToGetActiveClass() {
    driver.get(fixture("dynamic-page.html"));

    WebElement status = wait.until(d -> {
      WebElement el = d.findElement(By.id("status"));
      String classes = el.getAttribute("class");
      return classes != null && classes.contains("active") ? el : null;
    });

    assertEquals("Ready", status.getText());
  }

  @Test
  void fluentWait_customPollingInterval() {
    driver.get(fixture("dynamic-page.html"));

    Wait<WebDriver> fluentWait = new FluentWait<>(driver)
        .withTimeout(Duration.ofSeconds(30))
        .pollingEvery(Duration.ofSeconds(2))
        .ignoring(NoSuchElementException.class);

    WebElement element = fluentWait.until(d ->
        d.findElement(By.cssSelector(".search-result")));

    assertTrue(element.isDisplayed());
  }

  @Test
  void iframe_switchInInteractAndSwitchBack() {
    driver.get(fixture("iframe-page.html"));

    driver.switchTo().frame("inner-frame");
    driver.findElement(By.id("inside-frame")).sendKeys("text");
    assertTrue(driver.findElement(By.id("inside-button")).isDisplayed());

    // Forget this and every findElement below runs in the wrong context.
    driver.switchTo().defaultContent();
    assertTrue(driver.findElement(By.tagName("h1")).isDisplayed());
  }
}
