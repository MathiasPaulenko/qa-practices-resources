from steplib.behave import autoload


def before_all(context):
    """Load all installed behave-steplib plugins."""
    context.steplib = autoload(context)


def before_scenario(context, scenario):
    """Reset per-scenario state."""
    context.steplib.reset()


def after_scenario(context, scenario):
    """Clean up per-scenario state."""
    context.steplib.cleanup()
