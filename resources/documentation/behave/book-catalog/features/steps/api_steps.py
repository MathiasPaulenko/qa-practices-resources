# features/steps/api_steps.py
from behave import given, when, then, register_type
from api_client import BookAPIClient
from book_server import store
import parse


@parse.with_pattern(r'available|unavailable')
def parse_availability(text):
    return text == 'available'


register_type(Availability=parse_availability)


@given('the API catalog contains the following books:')
def step_api_catalog_contains_table(context):
    store.clear()
    for row in context.table:
        title = row['Title']
        available = row['Available'].lower() == 'true'
        store.add(title, available=available)


@when('I request the book "{title}"')
def step_request_book(context, title):
    client = BookAPIClient(context.base_url)
    context.response = client.get_book(title)


@then('the API returns {status:d}')
def step_api_returns_status(context, status):
    assert context.response.status_code == status, (
        f'Expected HTTP {status}, got {context.response.status_code}'
    )


@then('the response shows it is {availability:Availability}')
def step_response_shows_availability(context, availability):
    payload = context.response.json()
    actual = payload.get('available')
    assert actual == availability, f'Expected available={availability}, got {actual}'
