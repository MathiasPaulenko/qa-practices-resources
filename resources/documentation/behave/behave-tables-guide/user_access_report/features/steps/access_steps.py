from behave import given, when, then
from behave_tables import wrap
from access_service import AccessService


@given('the system has the following users')
def step_impl(context):
    context.service = AccessService()
    table = wrap(context.table)
    for row in table.as_dicts():
        context.service.add(
            user=row["user"],
            role=row["role"],
            department=row["department"],
            active=row["active"].lower() == "true",
        )


@when('I list the active users in the "{department}" department')
def step_impl(context, department):
    records = context.service.by_department(department)
    rows = [{"user": r.user, "role": r.role, "department": r.department, "active": str(r.active).lower()}
            for r in records]
    context.report = wrap(_DictTable(rows))


@then('I should see the following report')
def step_impl(context):
    expected = wrap(context.table)
    assert context.report == expected, f"Report mismatch: {context.report.as_dicts()}"


@when('I export the report as CSV')
def step_impl(context):
    if not hasattr(context, "report"):
        rows = context.service.to_table_rows()
        context.report = wrap(_DictTable(rows))
    context.csv_output = context.report.to_csv()


@then('the CSV output should contain {count:d} active users')
def step_impl(context, count):
    imported = wrap(_DictTable.from_csv(context.csv_output))
    assert len(imported) == count


class _DictTable:
    def __init__(self, rows, headings=None):
        self.rows = rows
        self.headings = headings or list(rows[0].keys()) if rows else []

    @classmethod
    def from_csv(cls, csv_string):
        from behave_tables import TableWrapper
        tw = TableWrapper.from_csv(csv_string)
        return cls(tw.as_dicts(), tw.headers)
