from pytest_bdd import scenario, given, when, then, parsers


@scenario("features/cart.feature", "Apply a voucher discount")
def test_apply_voucher(state):
    pass


@given(parsers.parse('the catalog price for "{product}" is {price}'))
def catalog_price(state, product, price):
    state["catalog"][product] = float(price)


@given(parsers.parse('the cart contains {quantity} "{product}"'))
def cart_contains(state, quantity, product):
    state["cart"][product] = int(quantity)


@when(parsers.parse('I apply a {discount}% voucher'))
def apply_voucher(state, discount):
    state["discount"] = int(discount) / 100.0


@then(parsers.parse('the cart total should be {total}'))
def cart_total_should_be(state, total):
    price = state["catalog"]["book"]
    quantity = state["cart"]["book"]
    actual = price * quantity * (1 - state["discount"])
    assert round(actual, 2) == float(total)
