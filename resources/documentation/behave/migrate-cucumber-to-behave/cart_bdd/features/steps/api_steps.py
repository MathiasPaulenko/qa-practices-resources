import requests
from behave import given, when, then


@given('the API is available at "{base_url}"')
def step_api_available(context, base_url):
    context.base_url = base_url


@when('I GET "{path}"')
def step_get(context, path):
    headers = {}
    if hasattr(context, 'token') and context.token:
        headers['Authorization'] = f'Bearer {context.token}'
    context.response = requests.get(f'{context.base_url}{path}', headers=headers, timeout=10)


@then('the response status should be {status:d}')
def step_status(context, status):
    assert context.response.status_code == status, (
        f'Expected {status}, got {context.response.status_code}'
    )
