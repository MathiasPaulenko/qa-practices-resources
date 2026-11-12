import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.action.ViewActions.*
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers.*
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Test
import org.junit.runner.RunWith

/**
 * In-process UI test — Espresso 3.5+ (AndroidX Test 1.5+).
 * Lives in the app's androidTest source set; run with
 * ./gradlew connectedAndroidTest on an emulator or device.
 * No explicit waits: Espresso synchronizes with the UI thread
 * and idling resources automatically.
 */
@RunWith(AndroidJUnit4::class)
class LoginEspressoTest {

    @Test
    fun login_showsDashboard() {
        onView(withId(R.id.email))
            .perform(typeText("qa@staging.acme.dev"), closeSoftKeyboard())
        onView(withId(R.id.login)).perform(click())
        onView(withId(R.id.dashboard)).check(matches(isDisplayed()))
    }
}
