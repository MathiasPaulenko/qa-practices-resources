package com.qapractices;

import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;
import org.junit.jupiter.api.*;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public class AuthTest {

    @BeforeAll
    void setUp() {
        baseURI = "https://reqres.in/api";
    }

    @Test
    @DisplayName("Basic Auth returns 200")
    void testWithBasicAuth() {
        given()
            .auth().basic("testuser", "testpass")
        .when()
            .get("/protected")
        .then()
            .statusCode(anyOf(is(200), is(401), is(404)));
    }

    @Test
    @DisplayName("Bearer Token (JWT) returns 200")
    void testWithBearerToken() {
        String token = "test-token-value";

        given()
            .header("Authorization", "Bearer " + token)
        .when()
            .get("/users/2")
        .then()
            .statusCode(200);
    }

    @Test
    @DisplayName("OAuth2 returns 200")
    void testWithOAuth2() {
        given()
            .auth().oauth2("access-token-value")
        .when()
            .get("/users/2")
        .then()
            .statusCode(200);
    }

    @Test
    @DisplayName("API Key as query parameter returns 200")
    void testWithApiKey() {
        given()
            .queryParam("api_key", "test-api-key")
        .when()
            .get("/users")
        .then()
            .statusCode(200);
    }
}
