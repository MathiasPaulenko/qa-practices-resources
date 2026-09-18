"""axe-core + Selenium (Python) accessibility checks.

Requires a local Chrome/Chromium install — Selenium 4 manages the driver
automatically. Run: pytest -v
"""
from selenium import webdriver
from axe_selenium_python import Axe

ACCESSIBLE_PAGE = """
<html lang="en"><body><main>
  <h1>Login</h1>
  <form><label for="email">Email</label>
  <input id="email" type="email"><button type="submit">Sign in</button></form>
</main></body></html>
"""

PAGE_WITH_VIOLATIONS = """
<html><body><div>
  <h3>Welcome</h3><img src="logo.png">
  <input type="text" placeholder="Search">
  <p style="color:#aaa">Low contrast text</p>
</div></body></html>
"""


def _driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    return webdriver.Chrome(options=options)


def test_accessible_page_has_no_violations():
    driver = _driver()
    try:
        driver.get("data:text/html," + ACCESSIBLE_PAGE)
        axe = Axe(driver)
        axe.inject()
        results = axe.run()
        assert len(results["violations"]) == 0, results["violations"]
    finally:
        driver.quit()


def test_broken_page_reports_image_alt_and_contrast():
    driver = _driver()
    try:
        driver.get("data:text/html," + PAGE_WITH_VIOLATIONS)
        axe = Axe(driver)
        axe.inject()
        results = axe.run()
        rule_ids = {v["id"] for v in results["violations"]}
        assert "image-alt" in rule_ids
        assert "color-contrast" in rule_ids
    finally:
        driver.quit()
