import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;

public class LoginPage {
  private final WebDriver driver;
  private final WebDriverWait wait;

  private final By emailInput = By.id("email");
  private final By passwordInput = By.id("password");
  private final By loginButton = By.cssSelector("[data-testid='login-button']");
  private final By errorMessage = By.id("error");

  public LoginPage(WebDriver driver) {
    this.driver = driver;
    this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  }

  public void enterEmail(String email) {
    driver.findElement(emailInput).sendKeys(email);
  }

  public void enterPassword(String password) {
    driver.findElement(passwordInput).sendKeys(password);
  }

  public void clickLogin() {
    driver.findElement(loginButton).click();
  }

  public String getErrorMessage() {
    return wait.until(
      ExpectedConditions.visibilityOfElementLocated(errorMessage)
    ).getText();
  }
}
