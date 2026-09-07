import XCTest

final class LoginPage {
    private let app: XCUIApplication

    init(app: XCUIApplication) {
        self.app = app
    }

    private var emailField: XCUIElement { app.textFields["emailInput"] }
    private var passwordField: XCUIElement { app.secureTextFields["passwordInput"] }
    private var loginButton: XCUIElement { app.buttons["loginButton"] }
    private var errorLabel: XCUIElement { app.staticTexts["Invalid credentials"] }
    private var welcomeLabel: XCUIElement { app.staticTexts["Welcome"] }

    func login(email: String, password: String) {
        emailField.tap()
        emailField.typeText(email)

        passwordField.tap()
        passwordField.typeText(password)

        if app.keyboards.buttons["Return"].exists {
            app.keyboards.buttons["Return"].tap()
        }

        XCTAssertTrue(loginButton.waitForExistence(timeout: 5))
        XCTAssertTrue(loginButton.isHittable)
        loginButton.tap()
    }

    func assertErrorMessageVisible() {
        XCTAssertTrue(errorLabel.waitForExistence(timeout: 5))
    }

    func assertWelcomeVisible() {
        XCTAssertTrue(welcomeLabel.waitForExistence(timeout: 5))
    }
}
