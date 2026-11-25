import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.emptyString;
import static org.hamcrest.Matchers.not;

import org.junit.jupiter.api.Test;

/**
 * Status code matrix examples with REST Assured 5.5 and JUnit 5.
 * Base URI comes from -DBASE_URL, defaults to a local stub.
 */
class StatusCodeMatrixTest {

    private static final String BASE_URL =
            System.getProperty("BASE_URL", "http://localhost:3000");

    @Test
    void getExistingUserReturns200() {
        given().baseUri(BASE_URL)
                .when().get("/users/1")
                .then().statusCode(200)
                .body(not(emptyString()));
    }

    @Test
    void createUserReturns201WithLocation() {
        given().baseUri(BASE_URL)
                .contentType("application/json")
                .body("{\"email\":\"qa@qapractices.com\",\"name\":\"QA\"}")
                .when().post("/users")
                .then().statusCode(201)
                .header("Location", containsString("/users/"));
    }

    @Test
    void missingAuthReturns401() {
        given().baseUri(BASE_URL)
                .when().get("/users")
                .then().statusCode(401);
    }

    @Test
    void wrongRoleReturns403() {
        given().baseUri(BASE_URL)
                .header("Authorization", "Bearer ${USER_TOKEN}")
                .when().get("/admin")
                .then().statusCode(403);
    }

    @Test
    void invalidPayloadReturns422() {
        given().baseUri(BASE_URL)
                .contentType("application/json")
                .body("{\"email\":\"not-an-email\"}")
                .when().post("/users")
                .then().statusCode(422);
    }
}
