from behave import given, when, then


@given('a registered user')
def step_registered_user(context):
    context.user = {"email": "qa@qapractices.com", "password": "secret"}


@given('the cart total is {total:f}')
def step_cart_total(context, total):
    context.total = total


@given('a previous charge of {amount:f}')
def step_previous_charge(context, amount):
    context.charge = amount


@given('there are completed payments')
def step_completed_payments(context):
    context.payments = [{"amount": 45.49, "status": "approved"}]


@when('the user logs in')
def step_user_logs_in(context):
    context.authenticated = True


@when('the user logs in with wrong password')
def step_wrong_password(context):
    # Simulates the buggy behaviour where the system authenticates a wrong
    # password. The Then step expects the login to fail.
    context.authenticated = True


@when('the card is charged')
def step_charge_card(context):
    context.payment_approved = context.total > 0


@when('the refund is requested')
def step_refund_requested(context):
    context.balance = context.charge


@when('the summary is generated')
def step_summary_generated(context):
    context.report = context.payments


@then('the user should be authenticated')
def step_authenticated(context):
    assert context.authenticated


@then('the login should fail')
def step_login_fail(context):
    assert not getattr(context, "authenticated", False), "login should have failed"


@then('the payment should be approved')
def step_payment_approved(context):
    assert context.payment_approved


@then('the balance should be {expected:f}')
def step_balance(context, expected):
    assert context.balance == expected


@then('the report should contain payments')
def step_report_payments(context):
    assert len(context.report) > 0
