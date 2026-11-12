import pytest
from pages.checkout_page import CheckoutPage
from utils.test_data_loader import TestDataLoader

@pytest.mark.regression
@pytest.mark.parallel
class TestCheckout:

    def test_checkout_with_invalid_card(self, driver, base_url):
        checkout = CheckoutPage(driver, base_url)
        checkout.open("/checkout")

        product = TestDataLoader.get_product("valid_sku")
        checkout.add_product(product)
        checkout.proceed_to_checkout()

        checkout.fill_payment({
            "card_number": "0000000000000000",
            "expiry": "12/28",
            "cvv": "123"
        })
        checkout.place_order()

        error = checkout.get_payment_error()
        assert error is not None, "No error for invalid card"
        assert "declined" in error.lower() or "invalid" in error.lower()
