package support;

import java.util.Map;

public class LoginPage {
    private static final Map<String, String> USERS = Map.of(
        "jane@qapractices.com", "SecurePass123!"
    );

    private String email = "";
    private String password = "";
    private String message = "";
    private boolean onDashboard = false;

    public void navigateTo() {
        email = "";
        password = "";
        message = "";
        onDashboard = false;
    }

    public void enterEmail(String value) {
        this.email = value;
    }

    public void enterPassword(String value) {
        this.password = value;
    }

    public void clickButton(String name) {
        if (!"login".equalsIgnoreCase(name)) {
            return;
        }
        if (email.isEmpty()) {
            message = "Email is required";
            return;
        }
        if (!USERS.containsKey(email)) {
            message = "User not found";
            return;
        }
        if (!USERS.get(email).equals(password)) {
            message = "Invalid credentials";
            return;
        }
        message = "Welcome";
        onDashboard = true;
    }

    public void loginWithSso() {
        message = "Welcome";
        onDashboard = true;
    }

    public String getMessage() {
        return message;
    }

    public boolean isDashboardVisible() {
        return onDashboard;
    }
}
