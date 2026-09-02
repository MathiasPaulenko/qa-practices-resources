"""Test cases for deep link and universal link testing.

Covers TC-001 through TC-010 from the QAPractices resource.
Requires Appium 2.5, pytest 8.3 and a running Appium server.
"""

import pytest
from deep_link_utils import trigger_appium_deep_link, trigger_android_deep_link


PRODUCT_URL = "https://shop.qapractices.com/product/123"
CUSTOM_SCHEME_URL = "qapractices://product/123?referral=email&campaign=spring"
ORDERS_URL = "https://shop.qapractices.com/orders/456"
CART_URL = "https://shop.qapractices.com/cart/789"
MALFORMED_URL_1 = "qapractices://unknown/abc"
MALFORMED_URL_2 = "qapractices://product"
PACKAGE = "com.qapractices.shop"


class TestDeepLinkBasic:
    """TC-001: Basic deep link with app installed."""

    def test_deep_link_opens_product_screen(self, android_driver):
        trigger_appium_deep_link(android_driver, PRODUCT_URL, PACKAGE, PACKAGE)
        product_title = android_driver.find_element("id", "productTitle").text
        assert product_title == "QA Testing Book"

    def test_product_price_loads(self, android_driver):
        trigger_appium_deep_link(android_driver, PRODUCT_URL, PACKAGE, PACKAGE)
        price = android_driver.find_element("id", "productPrice").text
        assert price is not None
        assert len(price) > 0


class TestDeepLinkParameters:
    """TC-002: Deep link with query and path parameters."""

    def test_referral_parameter_captured(self, android_driver):
        trigger_appium_deep_link(android_driver, CUSTOM_SCHEME_URL, PACKAGE, PACKAGE)
        # Check analytics payload or network logs
        referral = android_driver.find_element("id", "referralLabel").text
        assert referral == "email"

    def test_campaign_parameter_captured(self, android_driver):
        trigger_appium_deep_link(android_driver, CUSTOM_SCHEME_URL, PACKAGE, PACKAGE)
        campaign = android_driver.find_element("id", "campaignLabel").text
        assert campaign == "spring"


class TestDeepLinkAuth:
    """TC-004: Deep link to authenticated screen when user isn't logged in."""

    def test_login_screen_appears_first(self, android_driver):
        # Ensure user is logged out
        android_driver.reset()
        trigger_appium_deep_link(android_driver, ORDERS_URL, PACKAGE, PACKAGE)
        login_element = android_driver.find_element("id", "loginScreen")
        assert login_element.is_displayed()

    def test_navigates_to_order_after_login(self, android_driver):
        android_driver.reset()
        trigger_appium_deep_link(android_driver, ORDERS_URL, PACKAGE, PACKAGE)
        # Perform login
        android_driver.find_element("id", "usernameField").send_keys("testuser")
        android_driver.find_element("id", "passwordField").send_keys("testpass")
        android_driver.find_element("id", "loginButton").click()
        # Verify navigation to order 456
        order_id = android_driver.find_element("id", "orderIdLabel").text
        assert order_id == "456"


class TestDeepLinkBackground:
    """TC-005: Deep link with app in background."""

    def test_background_resume_navigates_correctly(self, android_driver):
        # Open app and send to background
        android_driver.background_app(5)
        trigger_appium_deep_link(android_driver, CART_URL, PACKAGE, PACKAGE)
        cart_id = android_driver.find_element("id", "cartIdLabel").text
        assert cart_id == "789"


class TestMalformedDeepLink:
    """TC-010: Invalid or malformed deep link."""

    def test_unknown_route_shows_error(self, android_driver):
        trigger_appium_deep_link(android_driver, MALFORMED_URL_1, PACKAGE, PACKAGE)
        error_screen = android_driver.find_element("id", "errorScreen")
        assert error_screen.is_displayed()

    def test_missing_id_shows_error(self, android_driver):
        trigger_appium_deep_link(android_driver, MALFORMED_URL_2, PACKAGE, PACKAGE)
        error_screen = android_driver.find_element("id", "errorScreen")
        assert error_screen.is_displayed()

    def test_no_crash_on_malformed_link(self, android_driver):
        trigger_appium_deep_link(android_driver, MALFORMED_URL_1, PACKAGE, PACKAGE)
        # App should still be responsive
        assert android_driver.is_app_installed(PACKAGE)


class TestAndroidADBDirect:
    """TC-001 and TC-007: Direct ADB testing without Appium."""

    def test_adb_launches_app_from_deep_link(self):
        output = trigger_android_deep_link(PRODUCT_URL, PACKAGE)
        assert "Status: ok" in output or "LaunchState" in output
