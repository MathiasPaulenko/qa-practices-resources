@api
Feature: Checkout API
  As a registered API client
  I want to submit checkout requests
  So that orders are processed programmatically

  @smoke
  Scenario: Successful checkout with valid cart
    Given a cart with product SKU "SKU-12345"
    When the user requests checkout for cart "cart-001"
    Then the checkout response status should be 200
    And the order total should be 99.99

  @regression
  Scenario: Checkout with empty cart
    Given a cart with product SKU ""
    When the user requests checkout for cart "cart-empty"
    Then the checkout response status should be 400
