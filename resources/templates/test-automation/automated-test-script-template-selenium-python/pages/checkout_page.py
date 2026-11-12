from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    # Locators
    ADD_TO_CART = (By.CSS_SELECTOR, ".add-to-cart")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    ORDER_CONFIRMATION = (By.CSS_SELECTOR, ".order-confirmed")
    ORDER_NUMBER = (By.CSS_SELECTOR, ".order-number")
    PAYMENT_ERROR = (By.CSS_SELECTOR, ".payment-error")
    CARD_NUMBER = (By.ID, "card-number")
    CARD_EXPIRY = (By.ID, "card-expiry")
    CARD_CVV = (By.ID, "card-cvv")

    def add_product(self, sku):
        self.click((By.CSS_SELECTOR, f"[data-sku='{sku}'] {self.ADD_TO_CART[1]}"))

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)

    def fill_payment(self, payment):
        self.type_text(self.CARD_NUMBER, payment["card_number"])
        self.type_text(self.CARD_EXPIRY, payment["expiry"])
        self.type_text(self.CARD_CVV, payment["cvv"])

    def place_order(self):
        self.click((By.ID, "place-order"))

    def is_order_confirmed(self):
        return self.is_visible(self.ORDER_CONFIRMATION)

    def get_order_number(self):
        if self.is_visible(self.ORDER_NUMBER):
            return self.get_text(self.ORDER_NUMBER)
        return None

    def get_payment_error(self):
        if self.is_visible(self.PAYMENT_ERROR):
            return self.get_text(self.PAYMENT_ERROR)
        return None
