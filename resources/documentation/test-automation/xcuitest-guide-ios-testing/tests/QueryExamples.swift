import XCTest

final class QueryExamples: XCTestCase {
    var app: XCUIApplication!

    override func setUp() {
        super.setUp()
        app = XCUIApplication()
        app.launch()
    }

    func testQueryByAccessibilityIdentifier() {
        let button = app.buttons["settingsButton"]
        XCTAssertTrue(button.exists)
    }

    func testQueryByText() {
        let label = app.staticTexts["Welcome"]
        XCTAssertTrue(label.exists)
    }

    func testQueryByIndex() {
        let firstCell = app.cells.element(boundBy: 0)
        XCTAssertTrue(firstCell.exists)
    }

    func testQueryChildren() {
        let cell = app.cells["userCell"]
        let nameLabel = cell.staticTexts["userName"]
        XCTAssertTrue(nameLabel.exists)
    }

    func testQueryFirstMatch() {
        let firstButton = app.buttons.firstMatch
        XCTAssertTrue(firstButton.exists)
    }
}
