import logging
import sys

from behave_priority import (
    setup_priority,
    before_scenario_hook,
    after_scenario_hook,
    priority_report,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    stream=sys.stdout,
)


def before_all(context):
    setup_priority(
        context,
        order=True,
        stop_after_failures=1,
        stop_on_critical=True,
        report=True,
    )


def before_scenario(context, scenario):
    before_scenario_hook(context, scenario)


def after_scenario(context, scenario):
    after_scenario_hook(context, scenario)


def after_all(context):
    priority_report(context)
