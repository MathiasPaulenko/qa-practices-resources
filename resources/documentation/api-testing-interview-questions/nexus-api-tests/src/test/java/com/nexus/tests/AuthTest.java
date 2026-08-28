package com.nexus.tests;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

import java.util.Base64;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

/**
 * JWT and OAuth 2.0 authentication tests for Nexus Payments.
 * Covers Q17 (JWT), Q18 (OAuth 2.0 grants), Q19 (API security).
 */
@Tag("smoke")
public class AuthTest {

    @BeforeAll
    static void configure() {
        RestAssured.baseURI = System.getProperty("base.url", "https://api.qa.io");
        RestAssured.basePath = "/v2";
    }

    @Test
    void jwtContainsRequiredClaims() {
        String token = loginAndGetToken("ana.lopez", "ValidPass123");

        String[] parts = token.split("\\.");
        String payload = new String(Base64.getUrlDecoder().decode(parts[1]));

        // Verify the token has exp, iss, sub, and merchant_id claims
        org.json.JSONObject json = new org.json.JSONObject(payload);

        assert json.has("exp") : "Token missing exp claim";
        assert json.has("iss") : "Token missing iss claim";
        assert json.has("sub") : "Token missing sub claim";
        assert json.has("merchant_id") : "Token missing merchant_id claim";
        assert json.getLong("exp") > System.currentTimeMillis() / 1000 : "Token already expired";
    }

    @Test
    void expiredTokenReturns401() {
        // A token with exp in the past
        String expiredToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibWVyY2hhbnRfaWQiOiJtXzAwMSIsImV4cCI6MTcwMDAwMDAwMH0.invalid";

        given()
            .header("Authorization", "Bearer " + expiredToken)
        .when()
            .get("/users/me")
        .then()
            .statusCode(401);
    }

    @Test
    void tamperedSignatureRejected() {
        String token = loginAndGetToken("ana.lopez", "ValidPass123");

        // Tamper with the signature
        String[] parts = token.split("\\.");
        String tampered = parts[0] + "." + parts[1] + ".tampered_signature";

        given()
            .header("Authorization", "Bearer " + tampered)
        .when()
            .get("/users/me")
        .then()
            .statusCode(401);
    }

    @Test
    void missingTokenReturns401() {
        given()
        .when()
            .get("/users/me")
        .then()
            .statusCode(401);
    }

    @Test
    void invalidCredentialsReturn401() {
        given()
            .contentType(ContentType.JSON)
            .body("{\"username\":\"ana.lopez\",\"password\":\"WrongPass\"}")
        .when()
            .post("/auth/login")
        .then()
            .statusCode(401);
    }

    @Test
    void errorDoesNotLeakStackTrace() {
        given()
            .contentType(ContentType.JSON)
            .body("{\"username\":\"ana.lopez\",\"password\":\"WrongPass\"}")
        .when()
            .post("/auth/login")
        .then()
            .statusCode(401)
            .body("error", not(containsString("java.")))
            .body("error", not(containsString("org.")))
            .body("error", not(containsString("com.nexus")));
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
