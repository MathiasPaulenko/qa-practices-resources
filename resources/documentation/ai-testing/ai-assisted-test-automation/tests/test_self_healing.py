"""Tests for the self-healing fallback locator — no browser required.

The FakeDriver mimics Selenium's find_element contract so the healing
logic can be verified in CI without spinning up WebDriver.
"""

import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from src.self_healing import find_with_fallback


class FakeDriver:
    """Returns an element only for selectors present in `known`."""

    def __init__(self, known):
        self.known = set(known)

    def find_element(self, by, selector):
        if selector in self.known:
            return f"element<{selector}>"
        raise NoSuchElementException(f"no such element: {selector}")


def test_primary_selector_hits_first():
    driver = FakeDriver({"#login-btn", "[data-testid='login']"})
    el = find_with_fallback(driver, "#login-btn", ["[data-testid='login']"])
    assert el == "element<#login-btn>"


def test_falls_back_when_primary_missing():
    driver = FakeDriver({"[data-testid='login']"})
    el = find_with_fallback(driver, "#login-btn", ["[data-testid='login']"])
    assert el == "element<[data-testid='login']>"


def test_tries_fallbacks_in_order():
    driver = FakeDriver({".btn-secondary"})
    el = find_with_fallback(
        driver, "#login-btn", ["[data-testid='login']", ".btn-secondary"]
    )
    assert el == "element<.btn-secondary>"


def test_raises_when_everything_misses():
    driver = FakeDriver(set())
    with pytest.raises(NoSuchElementException):
        find_with_fallback(driver, "#gone", ["#also-gone"])
