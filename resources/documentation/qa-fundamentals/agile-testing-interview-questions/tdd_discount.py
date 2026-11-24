"""TDD red-green-refactor example: loyal customer discount."""


# Red — write the test first
def test_discount_for_loyal_customer():
    customer = Customer(years=5)
    assert calculate_discount(customer) == 0.15


# Green — write minimum code to pass
def calculate_discount(customer):
    if customer.years >= 5:
        return 0.15
    return 0.0


class Customer:
    def __init__(self, years):
        self.years = years


# Refactor — improve while tests stay green
if __name__ == "__main__":
    test_discount_for_loyal_customer()
    print("TDD cycle complete: red -> green -> refactor")
