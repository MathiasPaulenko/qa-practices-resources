import pytest
from src.calculator import Calculator


def test_calculator_add(calculator):
    assert calculator.add(2, 3) == 5


def test_calculator_subtract(calculator):
    assert calculator.subtract(10, 4) == 6


def test_calculator_divide_by_zero(calculator):
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculator.divide(10, 0)


@pytest.mark.smoke
def test_calculator_smoke(calculator):
    assert calculator.add(1, 1) == 2
