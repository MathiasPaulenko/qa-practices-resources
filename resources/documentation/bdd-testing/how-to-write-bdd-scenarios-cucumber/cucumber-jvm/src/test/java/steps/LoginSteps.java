package steps;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import support.LoginPage;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class LoginSteps {
    private final LoginPage loginPage = new LoginPage();

    @Given("I am on the login page")
    public void iAmOnTheLoginPage() {
        loginPage.navigateTo();
    }

    @When("I enter {string} in the email field")
    public void enterEmail(String email) {
        loginPage.enterEmail(email);
    }

    @When("I enter {string} in the password field")
    public void enterPassword(String password) {
        loginPage.enterPassword(password);
    }

    @When("I click the {string} button")
    public void clickButton(String buttonName) {
        loginPage.clickButton(buttonName);
    }

    @When("I log in with SSO")
    public void loginWithSso() {
        loginPage.loginWithSso();
    }

    @Then("I should see {string}")
    public void verifyMessage(String expectedMessage) {
        assertEquals(expectedMessage, loginPage.getMessage());
    }

    @Then("I should be redirected to the dashboard")
    public void verifyDashboardRedirect() {
        assertTrue(loginPage.isDashboardVisible());
    }

    @Then("I should see the dashboard")
    public void verifyDashboard() {
        assertTrue(loginPage.isDashboardVisible());
    }
}
