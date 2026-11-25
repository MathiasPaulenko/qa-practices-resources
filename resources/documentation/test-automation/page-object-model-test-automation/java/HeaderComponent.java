import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

public class HeaderComponent {
    WebDriver driver;

    @FindBy(css = ".header-logo")
    WebElement logo;

    @FindBy(css = ".search-bar")
    WebElement searchBar;

    @FindBy(css = ".cart-icon")
    WebElement cartIcon;

    public HeaderComponent(WebDriver driver) {
        this.driver = driver;
        PageFactory.initElements(driver, this);
    }

    public void search(String query) {
        searchBar.clear();
        searchBar.sendKeys(query);
        searchBar.sendKeys(Keys.ENTER);
    }

    public CartPage goToCart() {
        cartIcon.click();
        return new CartPage(driver);
    }
}
