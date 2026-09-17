package steps;

import io.cucumber.datatable.DataTable;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import support.Shop;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class CartSteps {
    private final Shop shop = new Shop();

    @Given("I am logged in as a registered user")
    public void loggedIn() {
    }

    @Given("I have an empty shopping cart")
    public void emptyCart() {
        shop.clearCart();
    }

    @Given("the following products exist:")
    public void productsExist(DataTable table) {
        for (Map<String, String> row : table.asMaps()) {
            shop.stockProduct(
                row.get("name"),
                Integer.parseInt(row.get("price")),
                Integer.parseInt(row.get("stock")));
        }
    }

    @When("I add {string} to the cart")
    public void addItem(String name) {
        shop.addToCart(name);
    }

    @When("I create an order with:")
    public void createOrder(DataTable table) {
        shop.createOrder(table.asMaps());
    }

    @Then("the cart should contain {int} item")
    public void cartCount(int expected) {
        assertEquals(expected, shop.itemCount());
    }

    @Then("the cart total should be {string}")
    public void cartTotal(String expected) {
        assertEquals(expected, shop.totalFormatted());
    }

    @Then("the order total should be {string}")
    public void orderTotal(String expected) {
        assertEquals(expected, shop.totalFormatted());
    }
}
