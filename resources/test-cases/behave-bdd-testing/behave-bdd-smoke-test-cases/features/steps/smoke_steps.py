"""Step definitions for the smoke wiring checks (behave 1.3.3)."""

from behave import given


@given("the smoke context is initialized")
def step_smoke_context(context):
    assert context.global_flag is True, "before_all did not run"


@given("the following users exist")
def step_users_table(context):
    assert context.table.headings == ["name", "role"]
    rows = [list(r.cells) for r in context.table.rows]
    assert rows == [["Alice", "admin"], ["Bob", "reader"]]


@given('I log in as "{username}" with role "{role}"')
def step_login_outline(context, username, role):
    assert username and role == "valid"


@given("a full login flow placeholder")
def step_full_login(context):
    pass
