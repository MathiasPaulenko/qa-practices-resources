import XCTest

/// XCUITest specs for the iOS-specific test cases.
/// Drop into your app's UI test target (Xcode 15+).
final class LifecycleTests: XCTestCase {

    /// Deny every system permission alert without touching it manually (TC-005/006).
    override func setUp() {
        continueAfterFailure = false
        addUIInterruptionMonitor(withDescription: "Permission Alert") { alert in
            alert.buttons["Don't Allow"].tap()
            return true
        }
    }

    /// TC-001: typed input and app state survive a background/foreground cycle.
    func testStatePreservedAcrossBackgrounding() throws {
        let app = XCUIApplication()
        app.launch()

        app.textFields["searchField"].tap()
        app.typeText("wireless charger")

        XCUIDevice.shared.press(.home)
        app.activate()

        XCTAssertEqual(
            app.textFields["searchField"].value as? String,
            "wireless charger"
        )
    }

    /// TC-026: a universal link cold-starts into the deep-linked screen.
    func testUniversalLinkColdStart() throws {
        let app = XCUIApplication()
        app.terminate()

        // xcrun simctl openurl <device> "https://qapractices.example/orders/123"
        // or pass the URL via launch environment in CI.
        app.launchEnvironment["UL_TEST_URL"] = "https://qapractices.example/orders/123"
        app.launch()

        XCTAssertTrue(app.staticTexts["order_123_title"].waitForExistence(timeout: 5))
    }
}
