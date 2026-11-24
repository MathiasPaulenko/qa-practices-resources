// RecyclerViewMatcher: the withRecyclerView() helper the guide uses
// for assertions on rows without scrolling them into view.
// espresso-contrib ships RecyclerViewActions; this matcher is separate.
import android.view.View
import androidx.recyclerview.widget.RecyclerView
import androidx.test.espresso.matcher.BoundedMatcher
import org.hamcrest.Description
import org.hamcrest.Matcher

object RecyclerViewMatcher {

    fun withRecyclerView(recyclerViewId: Int) = RecyclerViewMatcherHelper(recyclerViewId)

    class RecyclerViewMatcherHelper(private val recyclerViewId: Int) {

        fun atPosition(position: Int): Matcher<View> =
            atPositionOnView(position, -1)

        fun atPositionOnView(position: Int, targetViewId: Int): Matcher<View> =
            object : BoundedMatcher<View, RecyclerView>(RecyclerView::class.java) {

                override fun describeTo(description: Description) {
                    description.appendText("has item at position $position in recycler view: ")
                    description.appendText("with id $recyclerViewId")
                }

                override fun matchesSafely(view: RecyclerView): Boolean {
                    val viewHolder = view.findViewHolderForAdapterPosition(position) ?: return false
                    val targetView = if (targetViewId == -1) {
                        viewHolder.itemView
                    } else {
                        viewHolder.itemView.findViewById(targetViewId)
                    }
                    return targetView != null
                }
            }
    }
}
