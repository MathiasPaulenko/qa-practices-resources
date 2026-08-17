"""Environment hooks for the payment reports demo."""


def before_all(context):
    context.config.reports_dir = "reports"
