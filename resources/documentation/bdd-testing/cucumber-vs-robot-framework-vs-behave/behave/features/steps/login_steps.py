import requests
from behave import given, when, then

BASE = "http://127.0.0.1:8080"

@given('a user account exists with "{email}" and "{password}"')
def step_create_account(context, email, password):
    resp = requests.post(f"{BASE}/api/v1/test-users", json={"email": email, "password": password})
    assert resp.status_code in (200, 409), f"Unexpected status {resp.status_code}"

@when('"{email}" logs in through the API with "{password}"')
def step_login(context, email, password):
    context.login_response = requests.post(
        f"{BASE}/api/v1/auth/login",
        json={"email": email, "password": password}
    )
    context.token = context.login_response.json().get("token")

@then('the API should respond with {status:d} and a token')
def step_assert_login(context, status):
    assert context.login_response.status_code == status
    assert context.token, "No token returned"

@when('the user requests the dashboard with the token')
def step_dashboard(context):
    context.dashboard_response = requests.get(
        f"{BASE}/api/v1/dashboard",
        headers={"Authorization": f"Bearer {context.token}"}
    )

@then('the dashboard should respond with {status:d} and "{text}"')
def step_assert_dashboard(context, status, text):
    assert context.dashboard_response.status_code == status
    assert text in context.dashboard_response.text
