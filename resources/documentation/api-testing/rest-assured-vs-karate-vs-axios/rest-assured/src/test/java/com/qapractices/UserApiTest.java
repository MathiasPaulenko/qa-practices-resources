package com.qapractices;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.equalTo;

import org.junit.jupiter.api.Test;

/**
 * The same "GET user by id" scenario as the Karate and Axios examples,
 * written with REST Assured 5.5.x and JUnit 5.
 */
public class UserApiTest {

    private static final String BASE_URI = "https://jsonplaceholder.typicode.com";

    @Test
    void shouldReturnUserWhenAuthorized() {
        given()
            .baseUri(BASE_URI)
            .header("Accept", "application/json")
        .when()
            .get("/users/1")
        .then()
            .statusCode(200)
            .body("id", equalTo(1))
            .body("email", containsString("@"))
            .body("username", equalTo("Bret"));
    }

    @Test
    void shouldReturn404ForUnknownUser() {
        given()
            .baseUri(BASE_URI)
        .when()
            .get("/users/999999")
        .then()
            .statusCode(404);
    }
}
