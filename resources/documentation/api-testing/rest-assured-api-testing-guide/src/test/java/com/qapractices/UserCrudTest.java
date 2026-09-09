package com.qapractices;

import static io.restassured.RestAssured.*;
import static io.restassured.module.jsv.JsonSchemaValidator.matchesJsonSchemaInClasspath;
import static org.hamcrest.Matchers.*;
import org.junit.jupiter.api.*;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class UserCrudTest {

    private static int createdUserId;

    @BeforeAll
    void setUp() {
        baseURI = "https://reqres.in/api";
    }

    @Test
    @Order(1)
    @DisplayName("Create user with POST")
    void createUser() {
        createdUserId = given()
            .header("Content-Type", "application/json")
            .body("""
                {
                  "name": "Jane Doe",
                  "job": "QA Engineer"
                }
                """)
        .when()
            .post("/users")
        .then()
            .statusCode(201)
            .body("id", notNullValue())
            .body("name", equalTo("Jane Doe"))
            .extract()
            .path("id");
    }

    @Test
    @Order(2)
    @DisplayName("Verify created user with GET")
    void verifyUser() {
        given()
            .pathParam("id", createdUserId)
        .when()
            .get("/users/{id}")
        .then()
            .statusCode(200)
            .body("data.id", equalTo(createdUserId));
    }

    @Test
    @Order(3)
    @DisplayName("Update user with PUT")
    void updateUser() {
        given()
            .header("Content-Type", "application/json")
            .pathParam("id", createdUserId)
            .body("""
                {
                  "name": "Jane Smith",
                  "job": "Senior QA Engineer"
                }
                """)
        .when()
            .put("/users/{id}")
        .then()
            .statusCode(200)
            .body("name", equalTo("Jane Smith"))
            .body("job", equalTo("Senior QA Engineer"));
    }

    @Test
    @Order(4)
    @DisplayName("Delete user with DELETE")
    void deleteUser() {
        given()
            .pathParam("id", createdUserId)
        .when()
            .delete("/users/{id}")
        .then()
            .statusCode(204);
    }

    @Test
    @DisplayName("Response matches user schema")
    void validateUserSchema() {
        given()
            .pathParam("id", 2)
        .when()
            .get("/users/{id}")
        .then()
            .statusCode(200)
            .body(matchesJsonSchemaInClasspath("schemas/user-schema.json"));
    }
}
