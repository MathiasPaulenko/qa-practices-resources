from behave import given, when, then

_attempts: dict[str, int] = {}


def _attempt(key: str) -> int:
    _attempts[key] = _attempts.get(key, 0) + 1
    return _attempts[key]


@given("the gateway is slow")
def step_slow_gateway(context):
    n = _attempt("slow_gateway")
    if n < 2:
        raise TimeoutError(f"Gateway timed out on attempt {n}")


@given("the gateway is responsive")
def step_responsive_gateway(context):
    context.total = 45.49


@given("the refund service is intermittent")
def step_refund_service(context):
    n = _attempt("refund_service")
    if n < 3:
        raise AssertionError(f"Refund failed on attempt {n}")
    context.balance = 45.49


@when("the card is charged")
def step_charge_card(context):
    context.payment_approved = True


@when("the refund is requested")
def step_refund_requested(context):
    pass


@then("the payment should be approved")
def step_payment_approved(context):
    assert context.payment_approved


@then("the balance should be {expected:f}")
def step_balance(context, expected):
    assert context.balance == expected
