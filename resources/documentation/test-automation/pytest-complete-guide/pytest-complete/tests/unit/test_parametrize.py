import pytest


@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (5, 5, 10),
    (-1, 1, 0),
    (0, 0, 0),
    (100, 200, 300),
])
def test_add_parametrized(calculator, a, b, expected):
    assert calculator.add(a, b) == expected


@pytest.mark.parametrize("email, is_valid", [
    ("user@example.com", True),
    ("invalid-email", False),
    ("", False),
    ("@example.com", False),
    ("user@", False),
])
def test_email_validation(email, is_valid):
    import re
    pattern = r"^[^@]+@[^@]+\.[^@]+$"
    assert (re.match(pattern, email) is not None) == is_valid
