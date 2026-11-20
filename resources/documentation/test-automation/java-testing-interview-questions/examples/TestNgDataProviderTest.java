import org.testng.Assert;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

/**
 * Mirrors Q9 of the Java Testing Interview guide:
 * TestNG @DataProvider feeding a @Test method.
 * Surefire runs this next to the JUnit 5 classes;
 * in a real suite you'd pick one engine.
 */
public class TestNgDataProviderTest {

    @DataProvider(name = "additionData")
    public Object[][] provideAdditionData() {
        return new Object[][] {
            {1, 2, 3},
            {0, 0, 0},
            {-1, 1, 0},
            {100, 200, 300}
        };
    }

    @Test(dataProvider = "additionData")
    public void testAdd(int a, int b, int expected) {
        Assert.assertEquals(Integer.sum(a, b), expected,
            "sum of " + a + " + " + b);
    }

    @DataProvider(name = "userData")
    public Object[][] provideUserData() {
        return new Object[][] {
            {"alice@test.com", true},
            {"not-an-email", false},
            {"bob@company", false}
        };
    }

    @Test(dataProvider = "userData")
    public void testEmailFormat(String email, boolean expected) {
        boolean valid = email.contains("@") && email.contains(".");
        Assert.assertEquals(valid, expected, email);
    }
}
