import pytest


def test_addition(calculator):
    assert calculator.add(2, 3) == 5


def test_subtraction(calculator):
    assert calculator.subtract(5, 3) == 2


def test_division_by_zero(calculator):
    with pytest.raises(ValueError, match="divide by zero"):
        calculator.divide(10, 0)


@pytest.mark.smoke
def test_smoke_addition(calculator):
    assert calculator.add(1, 1) == 2


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 5),
        (-1, 1, 0),
        (0, 0, 0),
        (100, 200, 300),
    ],
)
def test_addition_parametrized(a, b, expected, calculator):
    assert calculator.add(a, b) == expected
