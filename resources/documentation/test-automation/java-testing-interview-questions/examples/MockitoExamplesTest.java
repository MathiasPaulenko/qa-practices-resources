import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.contains;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.argThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.spy;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

/**
 * Mirrors Q10, Q11 and Q12 of the Java Testing Interview guide:
 * @Mock / @InjectMocks, when-thenReturn, verify, mock vs spy
 * and argument matchers.
 */
@ExtendWith(MockitoExtension.class)
class MockitoExamplesTest {

    interface UserRepository {
        User findById(int id);
        User save(User user);
        User findByEmail(String email);
        void deleteById(int id);
    }

    record User(int id, String name, String email) {}

    static class UserNotFoundException extends RuntimeException {
        UserNotFoundException(String message) { super(message); }
    }

    static class UserService {
        private final UserRepository repo;

        UserService(UserRepository repo) { this.repo = repo; }

        User getUserById(int id) {
            User user = repo.findById(id);
            if (user == null) {
                throw new UserNotFoundException("no user " + id);
            }
            return user;
        }
    }

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @Test
    @DisplayName("should return stubbed user by id")
    void shouldReturnStubbedUser() {
        User mockUser = new User(1, "Alice", "alice@test.com");
        when(userRepository.findById(1)).thenReturn(mockUser);

        User result = userService.getUserById(1);

        assertEquals("Alice", result.name());
        verify(userRepository, times(1)).findById(1);
    }

    @Test
    @DisplayName("should throw when repository returns null")
    void shouldThrowOnNull() {
        when(userRepository.findById(999)).thenReturn(null);

        assertThrows(UserNotFoundException.class,
            () -> userService.getUserById(999));

        verify(userRepository).findById(999);
    }

    @Test
    @DisplayName("mock returns defaults, spy runs real code")
    void mockVsSpy() {
        @SuppressWarnings("unchecked")
        List<String> mockList = mock(List.class);
        when(mockList.size()).thenReturn(10);
        assertEquals(10, mockList.size());

        List<String> spyList = spy(new ArrayList<>());
        spyList.add("item");
        assertEquals(1, spyList.size());
        when(spyList.size()).thenReturn(100);
        assertEquals(100, spyList.size());
    }

    @Test
    @DisplayName("argument matchers loosen stubbing and verification")
    void argumentMatchers() {
        User user = new User(2, "Bob", "bob@test.com");
        when(userRepository.findById(anyInt())).thenReturn(user);
        when(userRepository.findByEmail(contains("@test.com"))).thenReturn(user);
        when(userRepository.save(any(User.class))).thenReturn(user);

        assertEquals("Bob", userRepository.findById(42).name());
        assertEquals("Bob", userRepository.findByEmail("x@test.com").name());

        verify(userRepository).findById(eq(42));
        userRepository.save(user);
        verify(userRepository).save(argThat(u -> u.name().startsWith("B")));
    }
}
