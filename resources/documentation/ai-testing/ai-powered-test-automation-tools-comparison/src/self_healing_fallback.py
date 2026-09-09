"""Self-healing selector fallback for Selenium.

A lightweight helper that tries a primary selector, then falls back to
stable attributes before failing. This mirrors what AI self-healing tools
do, but keeps you in control of the fallback chain.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def find_with_fallback(driver, primary: str, fallbacks: list[str]):
    """Find an element using primary selector, then fallbacks.

    Args:
        driver: Selenium WebDriver instance.
        primary: Primary CSS selector.
        fallbacks: List of fallback CSS selectors ordered by stability.

    Returns:
        WebElement if found.

    Raises:
        NoSuchElementException: If no selector matches.
    """
    for selector in [primary] + fallbacks:
        try:
            return driver.find_element(By.CSS_SELECTOR, selector)
        except NoSuchElementException:
            continue
    raise NoSuchElementException(f"Could not find {primary} or any fallback")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    try:
        driver.get("https://qapractices.com")
        element = find_with_fallback(
            driver,
            primary="#submit-button",
            fallbacks=[
                '[data-testid="submit"]',
                'button[type="submit"]',
                'button:contains("Submit")',
            ],
        )
        print(f"Found element: {element.tag_name}")
    finally:
        driver.quit()
