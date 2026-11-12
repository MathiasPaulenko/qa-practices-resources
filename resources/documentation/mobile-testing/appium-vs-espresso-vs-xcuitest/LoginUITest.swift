import XCTest

/// Same login scenario in XCUITest (Xcode 15+).
/// The runner is a separate process driving the app through the
/// accessibility tree — element keys are accessibilityIdentifiers,
/// not visible labels. Run with:
/// xcodebuild test -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 16'
final class LoginUITest: XCTestCase {

    func testLoginShowsDashboard() throws {
        let app = XCUIApplication()
        app.launch()
        app.textFields["email"].tap()
        app.textFields["email"].typeText("qa@staging.acme.dev")
        app.buttons["login"].tap()
        XCTAssertTrue(app.staticTexts["Dashboard"].waitForExistence(timeout: 5))
    }
}
