from behave import given, then, when


@given('the inventory contains "{sku}" with quantity {qty:d}')
def step_inventory_contains(context, sku, qty):
    context.inventory.add(sku, qty)


@when('I reserve {qty:d} units of "{sku}"')
def step_reserve(context, qty, sku):
    context.inventory.reserve(sku, qty)


@then('the available quantity of "{sku}" should be {qty:d}')
def step_check_quantity(context, qty, sku):
    assert context.inventory.quantity(sku) == qty


@given('the cart contains "{sku}" priced at {price:f}')
def step_cart_add(context, sku, price):
    context.cart.add(sku, price)


@when('I calculate the total')
def step_calculate_total(context):
    context.total = context.cart.total()


@then('the total should be {expected:f}')
def step_check_total(context, expected):
    assert context.total == expected


@given('the cart total is {total:f}')
def step_cart_total(context, total):
    context.total = total


@when('I charge the card')
def step_charge_card(context):
    context.payment_approved = context.payment_gateway.charge(context.total)


@then('the payment should be approved')
def step_payment_approved(context):
    assert context.payment_approved
