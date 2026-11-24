// Page Object for the login screen.
// Centralizes locators so a layout change means editing one file.
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.action.ViewActions.*
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers.*

class LoginPage {
    private val emailInput = withId(R.id.email_input)
    private val passwordInput = withId(R.id.password_input)
    private val loginButton = withId(R.id.login_button)
    private val errorMessage = withText("Invalid credentials")

    fun login(email: String, password: String) {
        onView(emailInput).perform(typeText(email), closeSoftKeyboard())
        onView(passwordInput).perform(typeText(password), closeSoftKeyboard())
        onView(loginButton).perform(click())
    }

    fun assertErrorMessageVisible() {
        onView(errorMessage).check(matches(isDisplayed()))
    }

    fun assertDashboardVisible() {
        onView(withText("Welcome")).check(matches(isDisplayed()))
    }
}
