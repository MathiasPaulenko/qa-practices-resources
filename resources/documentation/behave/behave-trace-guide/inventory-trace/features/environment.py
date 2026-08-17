from behave_trace import attach_text, log


def before_scenario(context, scenario):
    log(context, f"Starting scenario: {scenario.name}", level="info")


def after_step(context, step):
    attach_text(
        context,
        f"Status: {step.status}, duration: {step.duration:.4f}s",
        name="step.txt",
    )
    if step.status == "failed":
        log(context, f"Step failed: {step.name}", level="error")
