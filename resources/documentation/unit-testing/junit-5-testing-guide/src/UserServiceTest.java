import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

class UserServiceTest {

    private UserService userService;

    @BeforeEach
    void setUp() {
        userService = new UserService();
    }

    @Nested
    @DisplayName("When creating a user")
    class WhenCreatingUser {

        @Test
        @DisplayName("creates user with valid data")
        void createsUserWithValidData() {
            User user = userService.create("Jane", "jane@example.com");
            assertNotNull(user);
            assertEquals("Jane", user.getName());
        }

        @Test
        @DisplayName("throws on invalid email")
        void throwsOnInvalidEmail() {
            assertThrows(IllegalArgumentException.class,
                () -> userService.create("Jane", "not-an-email"));
        }
    }

    @Nested
    @DisplayName("When updating a user")
    class WhenUpdatingUser {

        @Test
        @DisplayName("updates name successfully")
        void updatesNameSuccessfully() {
            User user = userService.create("Jane", "jane@example.com");
            userService.update(user.getId(), "Janet");
            assertEquals("Janet", userService.findById(user.getId()).getName());
        }
    }

    // Placeholder: replace with your real domain classes
    static class UserService {
        public User create(String name, String email) { return new User(name, email); }
        public void update(long id, String name) { /* placeholder */ }
        public User findById(long id) { return new User("Jane", "jane@example.com"); }
    }

    static class User {
        private final String name;
        private final String email;
        User(String name, String email) { this.name = name; this.email = email; }
        public String getName() { return name; }
        public long getId() { return 1; }
    }
}
