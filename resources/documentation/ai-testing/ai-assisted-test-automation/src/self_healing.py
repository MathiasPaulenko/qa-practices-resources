"""Minimal self-healing locator pattern.

Try a primary selector, then a list of stable fallbacks in order.
In production you'd log which fallback fired so a human can review it —
that's the audit trail commercial "self-healing" tools sell you.
"""

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def find_with_fallback(driver, primary, healed):
    """Try the primary selector, then stable fallbacks in order.

    Returns the located element. Raises NoSuchElementException when
    every candidate misses — never return a wrong element silently.
    """
    for selector in [primary] + healed:
        try:
            return driver.find_element(By.CSS_SELECTOR, selector)
        except NoSuchElementException:
            continue
    raise NoSuchElementException(primary)
