import java.util.UUID;

/**
 * Step 4 of the guide: fluent builder for test users.
 * No external dependencies — compiles with plain javac.
 */
public class UserBuilder {

    public record User(String id, String name, String email, String role, boolean active) {
    }

    private String id = UUID.randomUUID().toString();
    private String name = "Test User";
    private String email = "test@test.com";
    private String role = "user";
    private boolean active = true;

    public UserBuilder withName(String name) {
        this.name = name;
        return this;
    }

    public UserBuilder withEmail(String email) {
        this.email = email;
        return this;
    }

    public UserBuilder withRole(String role) {
        this.role = role;
        return this;
    }

    public UserBuilder inactive() {
        this.active = false;
        return this;
    }

    public User build() {
        return new User(id, name, email, role, active);
    }

    public static void main(String[] args) {
        User admin = new UserBuilder()
                .withName("John Doe")
                .withEmail("john@test.com")
                .withRole("admin")
                .build();
        User inactiveUser = new UserBuilder().inactive().build();

        System.out.println(admin);
        System.out.println(inactiveUser);

        if (!admin.role().equals("admin") || !admin.name().equals("John Doe")) {
            throw new AssertionError("Builder overrides did not apply");
        }
        if (inactiveUser.active()) {
            throw new AssertionError("inactive() did not flip the flag");
        }
        System.out.println("All builder checks passed");
    }
}
