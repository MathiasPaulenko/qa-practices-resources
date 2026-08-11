from behave_kit import (
    setup,
    setup_timeout,
    use_soft_asserts,
    timeout_before_scenario,
    timeout_after_scenario,
)


def before_all(context):
    setup(context)
    setup_timeout(context, default_timeout=30)


def before_scenario(context, scenario):
    use_soft_asserts(context)
    timeout_before_scenario(context, scenario)


def after_scenario(context, scenario):
    timeout_after_scenario(context, scenario)
