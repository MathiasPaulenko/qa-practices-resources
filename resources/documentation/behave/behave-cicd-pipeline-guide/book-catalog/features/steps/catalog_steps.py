from behave import given, when, then
from catalog_service import Catalog


@given('the catalog contains "{title}"')
def step_catalog_contains(context, title):
    if not hasattr(context, 'catalog'):
        context.catalog = Catalog()
    context.catalog.add(title)


@when('I search for "{title}"')
def step_search(context, title):
    context.results = context.catalog.search(title)


@then('I should find {count:d} book')
def step_should_find(context, count):
    assert len(context.results) == count, f"Expected {count}, got {len(context.results)}"
