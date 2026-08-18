from behave import step, when, then


@step('the customer adds "{title}" to the cart')
def step_add_to_cart(context, title):
    context.cart.add(title)


@when('a "{percent:d}%" discount is applied')
def step_apply_discount(context, percent):
    context.cart.apply_discount(percent)


@then('the cart total should be "${total:.2f}"')
def step_cart_total(context, total):
    actual = context.cart.discounted_total()
    assert actual == total, f"Expected cart total ${total}, got ${actual}"
