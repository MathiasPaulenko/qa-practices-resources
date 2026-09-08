// tests/LoginTests.swift
import XCTest

class LoginTests: XCTestCase {
    func testValidLogin() {
        let app = XCUIApplication()
        app.launch()
        app.textFields["email"].tap()
        app.textFields["email"].typeText("ana@qa.local")
        app.secureTextFields["password"].tap()
        app.secureTextFields["password"].typeText("ValidPass1")
        app.buttons["login"].tap()
        XCTAssertTrue(app.staticTexts["Welcome"].waitForExistence(timeout: 5))
    }

    func testInvalidLoginShowsError() {
        let app = XCUIApplication()
        app.launch()
        app.textFields["email"].tap()
        app.textFields["email"].typeText("ana@qa.local")
        app.secureTextFields["password"].tap()
        app.secureTextFields["password"].typeText("wrongpassword")
        app.buttons["login"].tap()
        XCTAssertTrue(app.staticTexts["Invalid email or password"].waitForExistence(timeout: 5))
    }
}
