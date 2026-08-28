package com.nexus.tests;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static io.restassured.RestAssured.given;
import static io.restassured.module.jsv.JsonSchemaValidator.matchesJsonSchemaInClasspath;
import static org.hamcrest.Matchers.*;

/**
 * Checkout endpoint tests for Nexus Payments v3.2.5.
 * Mirrors the 409 duplicate-charge incident from the interview guide.
 */
@Tag("smoke")
public class CheckoutTest {

    @BeforeAll
    static void configure() {
        RestAssured.baseURI = System.getProperty("base.url", "https://api.qa.io");
        RestAssured.basePath = "/v2";
    }

    @Test
    void happyPathCheckoutReturns201() {
        String idempotencyKey = UUID.randomUUID().toString();
        String token = getAuthToken("ana.lopez", "ValidPass123");

        given()
            .header("Authorization", "Bearer " + token)
            .header("Stripe-Idempotency-Key", idempotencyKey)
            .contentType(ContentType.JSON)
            .body("{\"merchant_id\":\"m_001\",\"amount\":4999,\"currency\":\"USD\"}")
        .when()
            .post("/checkout")
        .then()
            .statusCode(201)
            .body("payment_status", equalTo("completed"))
            .body("id", notNullValue())
            .time(lessThan(1500L));
    }

    @Test
    void duplicateChargeReturns409() {
        String idempotencyKey = "key_" + System.currentTimeMillis();
        String token = getAuthToken("ana.lopez", "ValidPass123");

        // First call succeeds
        given()
            .header("Authorization", "Bearer " + token)
            .header("Stripe-Idempotency-Key", idempotencyKey)
            .contentType(ContentType.JSON)
            .body("{\"merchant_id\":\"m_001\",\"amount\":4999,\"currency\":\"USD\"}")
        .when()
            .post("/checkout")
        .then()
            .statusCode(201);

        // Second call with same key must return 409
        given()
            .header("Authorization", "Bearer " + token)
            .header("Stripe-Idempotency-Key", idempotencyKey)
            .contentType(ContentType.JSON)
            .body("{\"merchant_id\":\"m_001\",\"amount\":4999,\"currency\":\"USD\"}")
        .when()
            .post("/checkout")
        .then()
            .statusCode(409)
            .body("error", containsString("duplicate"));
    }

    @Test
    void missingIdempotencyKeyRejected() {
        String token = getAuthToken("ana.lopez", "ValidPass123");

        given()
            .header("Authorization", "Bearer " + token)
            .contentType(ContentType.JSON)
            .body("{\"merchant_id\":\"m_001\",\"amount\":4999,\"currency\":\"USD\"}")
        .when()
            .post("/checkout")
        .then()
            .statusCode(400)
            .body("error", containsString("idempotency"));
    }

    @Test
    void checkoutSchemaValidation() {
        String token = getAuthToken("ana.lopez", "ValidPass123");

        given()
            .header("Authorization", "Bearer " + token)
            .header("Stripe-Idempotency-Key", UUID.randomUUID().toString())
            .contentType(ContentType.JSON)
            .body("{\"merchant_id\":\"m_001\",\"amount\":4999,\"currency\":\"USD\"}")
        .when()
            .post("/checkout")
        .then()
            .statusCode(201)
            .body(matchesJsonSchemaInClasspath("checkout-schema.json"));
    }

    @Test
    void expiredTokenReturns401() {
        given()
            .header("Authorization", "Bearer expired.token.here")
            .header("Stripe-Idempotency-Key", UUID.randomUUID().toString())
            .contentType(ContentType.JSON)
            .body("{\"merchant_id\":\"m_001\",\"amount\":4999,\"currency\":\"USD\"}")
        .when()
            .post("/checkout")
        .then()
            .statusCode(401);
    }

    @Test
    void crossMerchantAccessReturns403() {
        // User from merchant A tries to read merchant B's payment_intents
        String tokenMerchantA = getAuthToken("ana.lopez", "ValidPass123");

        given()
            .header("Authorization", "Bearer " + tokenMerchantA)
        .when()
            .get("/merchants/m_002/payment_intents")
        .then()
            .statusCode(403);
    }

    private String getAuthToken(String username, String password) {
        Response response = given()
            .contentType(ContentType.JSON)
            .body("{\"username\":\"" + username + "\",\"password\":\"" + password + "\"}")
        .when()
            .post("/auth/login");

        return response.jsonPath().getString("access_token");
    }
}
