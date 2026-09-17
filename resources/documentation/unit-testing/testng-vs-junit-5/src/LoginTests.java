import org.testng.Assert;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

public class LoginTests {

    @DataProvider(name = "credentials")
    public Object[][] credentials() {
        return new Object[][] {
            {"qa@example.com", "Str0ngP@ss!", true},
            {"bad@example.com", "wrong", false}
        };
    }

    @Test(dataProvider = "credentials")
    public void login(String email, String password, boolean expected) {
        boolean result = authService.login(email, password);
        Assert.assertEquals(result, expected);
    }

    // Placeholder: replace with your real service
    private final AuthService authService = new AuthService();

    static class AuthService {
        boolean login(String email, String password) {
            return email.contains("@") && password.length() > 5;
        }
    }
}
