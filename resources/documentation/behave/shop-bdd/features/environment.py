# features/environment.py
from shop_domain import Cart, DiscountEngine, Inventory, LoyaltyProgram, AlertService


def before_scenario(context, scenario):
    context.catalog = {}
    context.cart = Cart()
    context.discount_engine = DiscountEngine()
    context.inventory = Inventory()
    context.loyalty = LoyaltyProgram()
    context.alert_service = AlertService(context.inventory)
