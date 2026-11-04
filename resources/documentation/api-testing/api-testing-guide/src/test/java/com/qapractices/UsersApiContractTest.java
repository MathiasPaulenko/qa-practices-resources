package com.qapractices;

import static io.restassured.RestAssured.given;
import static io.restassured.module.jsv.JsonSchemaValidator.matchesJsonSchemaInClasspath;
import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.greaterThan;
import static org.hamcrest.Matchers.notNullValue;

import org.junit.jupiter.api.Test;

/**
 * Contract tests for GET /api/v1/users.
 *
 * Requires:
 *   API_BASE_URL  — defaults to https://staging.qapractices.com
 *   STAGING_TOKEN — bearer token for protected endpoints
 */
class UsersApiContractTest {

    private static final String BASE_URI =
            System.getenv().getOrDefault("API_BASE_URL", "https://staging.qapractices.com");

    private static final String TOKEN =
            System.getenv().getOrDefault("STAGING_TOKEN", "invalid-token");

    @Test
    void getUsersReturnsValidSchemaAndData() {
        given()
            .baseUri(BASE_URI)
            .header("Authorization", "Bearer " + TOKEN)
        .when()
            .get("/api/v1/users")
        .then()
            .statusCode(200)
            .body(matchesJsonSchemaInClasspath("schemas/users.json"))
            .body("data.size()", greaterThan(0))
            .body("data[0].email", containsString("@"));
    }

    @Test
    void getUsersWithInvalidTokenReturns401() {
        given()
            .baseUri(BASE_URI)
            .header("Authorization", "Bearer invalid-token")
        .when()
            .get("/api/v1/users")
        .then()
            .statusCode(401)
            .body("error", notNullValue());
    }

    @Test
    void getUserWithUnknownIdReturns404() {
        given()
            .baseUri(BASE_URI)
            .header("Authorization", "Bearer " + TOKEN)
        .when()
            .get("/api/v1/users/00000000-0000-0000-0000-000000000000")
        .then()
            .statusCode(404)
            .body("error", notNullValue());
    }
}
