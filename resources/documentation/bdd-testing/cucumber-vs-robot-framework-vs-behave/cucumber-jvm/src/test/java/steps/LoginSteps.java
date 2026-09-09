package steps;

import io.cucumber.java.en.*;
import io.restassured.RestAssured;
import io.restassured.response.Response;

import java.util.Map;

import static org.hamcrest.Matchers.anyOf;
import static org.hamcrest.Matchers.is;
import static org.junit.jupiter.api.Assertions.*;

public class LoginSteps {
    private static final String BASE = System.getProperty("api.base", "http://127.0.0.1:8080");
    private Response loginResponse;
    private Response dashboardResponse;
    private String token;

    @Given("a user account exists with {string} and {string}")
    public void createAccount(String email, String password) {
        RestAssured.given()
            .baseUri(BASE)
            .contentType("application/json")
            .body(Map.of("email", email, "password", password))
        .when()
            .post("/api/v1/test-users")
        .then()
            .statusCode(anyOf(is(200), is(409)));
    }

    @When("{string} logs in through the API with {string}")
    public void login(String email, String password) {
        loginResponse = RestAssured.given()
            .baseUri(BASE)
            .contentType("application/json")
            .body(Map.of("email", email, "password", password))
        .when()
            .post("/api/v1/auth/login")
        .thenReturn();
        token = loginResponse.jsonPath().getString("token");
    }

    @Then("the API should respond with {int} and a token")
    public void assertLogin(int expected) {
        assertEquals(expected, loginResponse.statusCode());
        assertNotNull(token, "Token was not returned");
    }

    @When("the user requests the dashboard with the token")
    public void requestDashboard() {
        dashboardResponse = RestAssured.given()
            .baseUri(BASE)
            .header("Authorization", "Bearer " + token)
        .when()
            .get("/api/v1/dashboard")
        .thenReturn();
    }

    @Then("the dashboard should respond with {int} and {string}")
    public void assertDashboard(int expected, String text) {
        assertEquals(expected, dashboardResponse.statusCode());
        assertTrue(dashboardResponse.asString().contains(text));
    }
}
