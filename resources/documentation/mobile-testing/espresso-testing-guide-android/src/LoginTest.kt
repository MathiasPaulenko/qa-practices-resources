// app/src/androidTest/java/com/example/app/LoginTest.kt
// Replace com.example.app, R.id.* and LoginActivity with your own.
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.espresso.Espresso.*
import androidx.test.espresso.action.ViewActions.*
import androidx.test.espresso.assertion.ViewAssertions.*
import androidx.test.espresso.matcher.ViewMatchers.*
import androidx.test.ext.junit.rules.ActivityScenarioRule
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class LoginTest {

    @get:Rule
    val activityRule = ActivityScenarioRule(LoginActivity::class.java)

    @Test
    fun loginWithValidCredentials_showsDashboard() {
        onView(withId(R.id.email_input))
            .perform(typeText("jane@example.com"), closeSoftKeyboard())
        onView(withId(R.id.password_input))
            .perform(typeText("validpass123"), closeSoftKeyboard())
        onView(withId(R.id.login_button))
            .perform(click())

        onView(withText("Welcome, Jane"))
            .check(matches(isDisplayed()))
    }

    @Test
    fun loginWithInvalidCredentials_showsError() {
        onView(withId(R.id.email_input))
            .perform(typeText("jane@example.com"), closeSoftKeyboard())
        onView(withId(R.id.password_input))
            .perform(typeText("wrongpass"), closeSoftKeyboard())
        onView(withId(R.id.login_button))
            .perform(click())

        onView(withText("Invalid credentials"))
            .check(matches(isDisplayed()))
    }
}
