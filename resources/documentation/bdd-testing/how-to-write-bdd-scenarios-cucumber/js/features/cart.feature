Feature: Shopping Cart

  Background:
    Given I am logged in as a registered user
    And I have an empty shopping cart

  @smoke
  Scenario: Add item to cart
    Given the following products exist:
      | name               | price | stock |
      | Wireless Headphones | 99   | 10    |
    When I add "Wireless Headphones" to the cart
    Then the cart should contain 1 item
    And the cart total should be "$99.00"

  @regression
  Scenario: Create order with multiple items
    Given the following products exist:
      | name     | price | stock |
      | Laptop   | 999   | 10    |
      | Mouse    | 25    | 50    |
      | Keyboard | 75    | 30    |
    When I create an order with:
      | product | quantity |
      | Laptop  | 1        |
      | Mouse   | 2        |
    Then the order total should be "$1049.00"
