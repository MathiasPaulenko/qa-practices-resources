# features/steps/ui_steps.py
import parse
from behave import given, then, when, register_type
from playwright.sync_api import expect


@parse.with_pattern(r'available|unavailable')
def parse_availability(text):
    return text == 'available'


register_type(Availability=parse_availability)


@given('the catalog contains "{title}" marked as {availability:Availability}')
def step_catalog_contains(context, title, availability):
    context.store.add(title, available=availability)


@when('I search for "{title}" in the web catalog')
def step_search_web(context, title):
    context.page.goto(context.base_url)
    context.page.locator('#title').fill(title)
    context.page.locator('button[type="submit"]').click()


@then('the web result should show "{text}"')
def step_web_result(context, text):
    result = context.page.locator('#result')
    expect(result).to_contain_text(text)
