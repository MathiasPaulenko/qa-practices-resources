from behave import given, when, then


@given('the cart total is {total:f}')
def step_cart_total(context, total):
    context.total = total
    context.balance = 100.0


@given('the card balance is {amount:f}')
def step_card_balance(context, amount):
    context.balance = amount


@given('a previous charge of {amount:f}')
def step_previous_charge(context, amount):
    context.charge = amount


@when('the card is charged')
def step_charge_card(context):
    context.payment_approved = context.total <= context.balance


@when('the refund is requested')
def step_refund_requested(context):
    context.balance = context.charge


@then('the payment should be approved')
def step_payment_approved(context):
    assert context.payment_approved


@then('the payment should be declined')
def step_payment_declined(context):
    assert not context.payment_approved


@then('the balance should be {expected:f}')
def step_balance(context, expected):
    assert context.balance == expected
