import java.time.Duration;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.WebDriverWait;

public class DashboardPage {
    WebDriver driver;
    WebDriverWait wait;

    @FindBy(id = "welcome-message")
    WebElement welcomeMessage;

    @FindBy(css = ".user-menu")
    WebElement userMenu;

    @FindBy(css = ".logout")
    WebElement logoutButton;

    public DashboardPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        PageFactory.initElements(driver, this);
    }

    public String getWelcomeMessage() {
        return welcomeMessage.getText();
    }

    public LoginPage logout() {
        userMenu.click();
        logoutButton.click();
        return new LoginPage(driver);
    }
}
