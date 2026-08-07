# features/steps/catalog_steps.py
import parse
from behave import given, when, then, register_type


@parse.with_pattern(r'available|unavailable')
def parse_availability(text):
    return text == 'available'


register_type(Availability=parse_availability)


@given('the catalog contains "{title}"')
def step_catalog_contains(context, title):
    context.catalog.add(title, available=True)


@given('the catalog contains "{title}" marked as {availability:Availability}')
def step_catalog_contains_availability(context, title, availability):
    context.catalog.add(title, available=availability)


@given('the catalog contains the following books:')
def step_catalog_contains_table(context):
    for row in context.table:
        title = row['Title']
        available = row['Available'].lower() == 'true'
        context.catalog.add(title, available=available)


@when('I search for "{title}"')
def step_search(context, title):
    context.results = context.catalog.search(title)


@then('I should find {count:d} {word}')
def step_should_find(context, count, word):
    actual = len(context.results)
    assert actual == count, f'Expected {count} {word}, found {actual}'


@then('the result should be {availability:Availability}')
def step_result_availability(context, availability):
    assert len(context.results) == 1
    actual = context.results[0].available
    assert actual == availability, f'Expected available={availability}, got {actual}'
