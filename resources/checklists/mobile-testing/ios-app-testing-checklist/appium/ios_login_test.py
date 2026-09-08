# appium/ios_login_test.py
"""Appium iOS login test using the XCUITest driver."""

from capabilities import create_driver


def test_valid_login():
    driver = create_driver("build/Products/Debug-iphonesimulator/QAPractices.app")
    try:
        email = driver.find_element("accessibility id", "email")
        email.click()
        email.send_keys("ana@qa.local")

        password = driver.find_element("accessibility id", "password")
        password.click()
        password.send_keys("ValidPass1")

        driver.find_element("accessibility id", "login").click()

        welcome = driver.find_element("accessibility id", "Welcome")
        assert welcome.is_displayed(), "Welcome text should appear after valid login"
    finally:
        driver.quit()


def test_invalid_login_shows_error():
    driver = create_driver("build/Products/Debug-iphonesimulator/QAPractices.app")
    try:
        email = driver.find_element("accessibility id", "email")
        email.click()
        email.send_keys("ana@qa.local")

        password = driver.find_element("accessibility id", "password")
        password.click()
        password.send_keys("wrongpassword")

        driver.find_element("accessibility id", "login").click()

        error = driver.find_element("accessibility id", "login-error")
        assert "Invalid email or password" in error.text
    finally:
        driver.quit()


if __name__ == "__main__":
    test_valid_login()
    test_invalid_login_shows_error()
    print("All iOS login tests passed.")
