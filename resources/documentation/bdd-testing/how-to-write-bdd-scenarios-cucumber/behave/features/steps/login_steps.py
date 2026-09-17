from behave import given, when, then


class LoginPage:
    USERS = {"jane@qapractices.com": "SecurePass123!"}

    def __init__(self):
        self.email = ""
        self.password = ""
        self.message = ""
        self.on_dashboard = False

    def navigate_to(self):
        self.email = ""
        self.password = ""
        self.message = ""
        self.on_dashboard = False

    def click_button(self, name):
        if name.lower() != "login":
            return
        if not self.email:
            self.message = "Email is required"
            return
        if self.email not in self.USERS:
            self.message = "User not found"
            return
        if self.USERS[self.email] != self.password:
            self.message = "Invalid credentials"
            return
        self.message = "Welcome"
        self.on_dashboard = True

    def login_with_sso(self):
        self.message = "Welcome"
        self.on_dashboard = True


@given('I am on the login page')
def step_on_login_page(context):
    context.page = LoginPage()
    context.page.navigate_to()


@when('I enter "{email}" in the email field')
def step_enter_email(context, email):
    context.page.email = email


@when('I enter "{password}" in the password field')
def step_enter_password(context, password):
    context.page.password = password


@when('I click the "{button_name}" button')
def step_click_button(context, button_name):
    context.page.click_button(button_name)


@when('I log in with SSO')
def step_login_sso(context):
    context.page.login_with_sso()


@then('I should see "{expected_message}"')
def step_verify_message(context, expected_message):
    assert context.page.message == expected_message


@then('I should be redirected to the dashboard')
def step_verify_dashboard(context):
    assert context.page.on_dashboard


@then('I should see the dashboard')
def step_see_dashboard(context):
    assert context.page.on_dashboard
