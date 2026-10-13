package com.qapractices.api;

import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.equalTo;

/**
 * Same assertions as postman/users-collection.postman_collection.json.
 * Override the target with -Dapi.url and API_KEY env var.
 */
class UserApiTest {

    private static final String BASE_URL =
            System.getProperty("api.url", "https://api.acme-retail.com");
    private static final String API_KEY = System.getenv("API_KEY");

    @Test
    void shouldReturnUserById() {
        given()
            .baseUri(BASE_URL)
            .header("X-API-Key", API_KEY)
            .pathParam("userId", 123)
        .when()
            .get("/users/{userId}")
        .then()
            .statusCode(200)
            .body("name", equalTo("Ana"))
            .body("email", containsString("@acme-retail.com"));
    }

    @Test
    void shouldRejectMissingApiKey() {
        given()
            .baseUri(BASE_URL)
        .when()
            .get("/users/123")
        .then()
            .statusCode(401);
    }

    @Test
    void shouldAnswerWithinTwoSeconds() {
        given()
            .baseUri(BASE_URL)
            .header("X-API-Key", API_KEY)
        .when()
            .get("/users/123")
        .then()
            .statusCode(200)
            .time(org.hamcrest.Matchers.lessThan(2000L));
    }
}
