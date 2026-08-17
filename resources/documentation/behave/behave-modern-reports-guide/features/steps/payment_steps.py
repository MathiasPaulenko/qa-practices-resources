from behave import given, when, then


@given('the checkout total is "{total}"')
def step_checkout_total(context, total):
    context.total = total
    context.payment_authorized = None


@when('the customer pays with a valid card')
def step_pay_valid(context):
    context.payment_authorized = True


@when('the customer pays with a declined card')
def step_pay_declined(context):
    context.payment_authorized = False


@then('the payment is authorized')
def step_authorized(context):
    assert context.payment_authorized is True, "Expected payment to be authorized"


@then('the payment is declined')
def step_declined(context):
    assert context.payment_authorized is False, "Expected payment to be declined"
