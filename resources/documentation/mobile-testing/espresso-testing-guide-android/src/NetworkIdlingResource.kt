// Custom IdlingResource for async work Espresso cannot see
// (Retrofit calls, coroutines, custom executors).
import androidx.test.espresso.IdlingResource

class NetworkIdlingResource(private val isLoading: () -> Boolean) : IdlingResource {
    private var resourceCallback: IdlingResource.ResourceCallback? = null

    override fun getName(): String = "NetworkIdlingResource"

    override fun isIdleNow(): Boolean {
        val idle = !isLoading()
        if (idle) {
            resourceCallback?.onTransitionToIdle()
        }
        return idle
    }

    override fun registerIdleTransitionCallback(callback: IdlingResource.ResourceCallback) {
        resourceCallback = callback
    }
}

// Usage inside a test:
//   val idlingResource = NetworkIdlingResource { viewModel.isLoading.value == true }
//   IdlingRegistry.getInstance().register(idlingResource)
//   ... perform actions and assertions ...
//   IdlingRegistry.getInstance().unregister(idlingResource)
