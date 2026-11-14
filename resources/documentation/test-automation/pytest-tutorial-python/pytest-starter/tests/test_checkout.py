import pytest
from checkout import calculate_total

ITEMS = [{"price": 100, "qty": 2}, {"price": 50, "qty": 1}]


def test_calculate_total_with_discount():
    assert calculate_total(ITEMS, discount=0.1) == pytest.approx(225.0)


def test_calculate_total_empty_cart():
    assert calculate_total([], discount=0) == 0


def test_calculate_total_invalid_discount():
    with pytest.raises(ValueError):
        calculate_total(ITEMS, discount=1.5)


@pytest.mark.parametrize(
    "discount,expected",
    [(0, 250), (0.1, 225), (0.5, 125)],
)
def test_calculate_total_parametrized(discount, expected):
    assert calculate_total(ITEMS, discount) == pytest.approx(expected)
