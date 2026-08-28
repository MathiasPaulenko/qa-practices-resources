package com.nexus.tests;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static io.restassured.module.jsv.JsonSchemaValidator.matchesJsonSchemaInClasspath;
import static org.hamcrest.Matchers.*;

/**
 * Contract testing for Nexus Payments API.
 * Covers Q12 (JSON Schema) and Q36 (contract testing).
 */
@Tag("smoke")
public class ContractTest {

    @BeforeAll
    static void configure() {
        RestAssured.baseURI = System.getProperty("base.url", "https://api.qa.io");
        RestAssured.basePath = "/v2";
    }

    @Test
    void userResponseMatchesSchema() {
        String token = loginAndGetToken("ana.lopez", "ValidPass123");

        given()
            .header("Authorization", "Bearer " + token)
        .when()
            .get("/users/123")
        .then()
            .statusCode(200)
            .body(matchesJsonSchemaInClasspath("user-schema.json"));
    }

    @Test
    void checkoutResponseMatchesSchema() {
        String token = loginAndGetToken("ana.lopez", "ValidPass123");

        given()
            .header("Authorization", "Bearer " + token)
            .header("Stripe-Idempotency-Key", java.util.UUID.randomUUID().toString())
            .contentType(ContentType.JSON)
            .body("{\"merchant_id\":\"m_001\",\"amount\":4999,\"currency\":\"USD\"}")
        .when()
            .post("/checkout")
        .then()
            .statusCode(201)
            .body(matchesJsonSchemaInClasspath("checkout-schema.json"));
    }

    @Test
    void paginationResponseHasRequiredFields() {
        String token = loginAndGetToken("ana.lopez", "ValidPass123");

        given()
            .header("Authorization", "Bearer " + token)
            .queryParam("page", 1)
            .queryParam("size", 10)
        .when()
            .get("/users")
        .then()
            .statusCode(200)
            .body("data", notNullValue())
            .body("page", equalTo(1))
            .body("size", equalTo(10))
            .body("total", notNullValue());
    }

    @Test
    void unsupportedFormatReturns406() {
        String token = loginAndGetToken("ana.lopez", "ValidPass123");

        given()
            .header("Authorization", "Bearer " + token)
            .header("Accept", "application/xml")
        .when()
            .get("/users/123")
        .then()
            .statusCode(anyOf(equalTo(406), equalTo(415)));
    }

    private String loginAndGetToken(String username, String password) {
        return given()
            .contentType(ContentType.JSON)
            .body("{\"username\":\"" + username + "\",\"password\":\"" + password + "\"}")
        .when()
            .post("/auth/login")
            .jsonPath()
            .getString("access_token");
    }
}
