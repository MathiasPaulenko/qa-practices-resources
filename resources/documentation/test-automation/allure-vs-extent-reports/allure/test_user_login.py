"""Same login scenario reported with Allure (allure-pytest 2.x).

Run:
    pip install -r requirements.txt
    pytest --alluredir=allure-results
    allure generate allure-results -o allure-report --clean
    allure serve allure-results   # live preview
"""
import allure
import pytest


class FakeLoginPage:
    """Placeholder page object — replace with your real page or API client."""

    def enter_credentials(self, user: str, password: str) -> None:
        self._user = user
        self._password = password

    def submit(self) -> None:
        self._submitted = True

    def dashboard_visible(self) -> bool:
        return getattr(self, "_submitted", False) and self._user == "demo"


@allure.feature("Authentication")
@allure.story("Login")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("layer", "ui")
class TestUserLogin:

    @allure.title("User logs in with valid credentials")
    def test_login_success(self):
        page = FakeLoginPage()

        with allure.step("Enter valid credentials"):
            page.enter_credentials("demo", "s3cret")  # Placeholder: use a test account

        with allure.step("Submit the form"):
            page.submit()

        with allure.step("Verify the dashboard is visible"):
            assert page.dashboard_visible()
            allure.attach(
                "dashboard rendered for user=demo",
                name="Observation",
                attachment_type=allure.attachment_type.TEXT,
            )

    @allure.title("Login fails with a locked account")
    def test_login_locked_account(self):
        page = FakeLoginPage()

        with allure.step("Enter credentials for a locked account"):
            page.enter_credentials("locked-user", "s3cret")

        with allure.step("Submit the form"):
            page.submit()

        with allure.step("Verify the dashboard is NOT visible"):
            assert not page.dashboard_visible()


@pytest.fixture(autouse=True)
def report_environment():
    """Attach environment context to every test in this module."""
    allure.dynamic.label("environment", "staging")
    yield
