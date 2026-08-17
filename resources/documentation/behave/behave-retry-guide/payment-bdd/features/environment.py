import logging
import sys

from behave_retry import (
    setup_retry,
    after_scenario_hook,
    retry_report,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    stream=sys.stdout,
)


def before_all(context):
    setup_retry(
        context,
        max_retries=2,
        retry_tags=["@flaky"],
        retry_on=[TimeoutError, AssertionError],
        retry_delay=1.0,
        backoff_factor=2.0,
    )


def after_scenario(context, scenario):
    after_scenario_hook(context, scenario)


def after_all(context):
    print(retry_report(context))
