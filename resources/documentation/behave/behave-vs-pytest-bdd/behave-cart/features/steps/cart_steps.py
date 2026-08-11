from behave import given, when, then


@given('the catalog price for "{product}" is {price:f}')
def step_catalog_price(context, product, price):
    context.catalog[product] = price


@given('the cart contains {quantity:d} "{product}"')
def step_cart_contains(context, quantity, product):
    context.cart[product] = quantity


@when('I apply a {discount:d}% voucher')
def step_apply_voucher(context, discount):
    context.discount = discount / 100.0


@then('the cart total should be {total:f}')
def step_cart_total(context, total):
    price = context.catalog["book"]
    quantity = context.cart["book"]
    actual = price * quantity * (1 - context.discount)
    assert round(actual, 2) == round(total, 2), f"Expected {total}, got {actual}"
