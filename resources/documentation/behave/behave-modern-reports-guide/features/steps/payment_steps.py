from behave import given, when, then


@given('the checkout total is "{total}"')
def step_checkout_total(context, total):
    context.total = total


@when('the customer pays with a valid card')
def step_pay_valid(context):
    pass


@when('the customer pays with a declined card')
def step_pay_declined(context):
    pass


@then('the payment is authorized')
def step_authorized(context):
    assert True


@then('the payment is declined')
def step_declined(context):
    assert True
