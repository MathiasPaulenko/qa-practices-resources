import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

public class ProductPage {
    @FindBy(css = ".header")
    WebElement headerElement;
    private HeaderComponent header;

    public ProductPage(WebDriver driver) {
        PageFactory.initElements(driver, this);
        header = new HeaderComponent(driver);
    }
}
