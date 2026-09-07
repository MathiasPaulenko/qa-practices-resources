import XCTest

final class LoginTests: XCTestCase {
    var app: XCUIApplication!
    var loginPage: LoginPage!

    override func setUp() {
        super.setUp()
        app = XCUIApplication()
        app.launchArguments = ["-UITests"]
        continueAfterFailure = false
        loginPage = LoginPage(app: app)
    }

    override func tearDown() {
        app = nil
        super.tearDown()
    }

    func testLoginSuccess() {
        app.launch()
        loginPage.login(email: "jane@example.com", password: "validpass123")
        loginPage.assertWelcomeVisible()
    }

    func testLoginFailure() {
        app.launch()
        loginPage.login(email: "jane@example.com", password: "wrongpass")
        loginPage.assertErrorMessageVisible()
    }

    func testLoginButtonDisabledUntilFormIsValid() {
        app.launch()

        let loginButton = app.buttons["loginButton"]
        let emailField = app.textFields["emailInput"]
        let passwordField = app.secureTextFields["passwordInput"]

        XCTAssertFalse(loginButton.isEnabled)

        emailField.tap()
        emailField.typeText("jane@example.com")

        passwordField.tap()
        passwordField.typeText("validpass123")

        XCTAssertTrue(loginButton.waitForExistence(timeout: 5))
        XCTAssertTrue(loginButton.isEnabled)
    }
}
