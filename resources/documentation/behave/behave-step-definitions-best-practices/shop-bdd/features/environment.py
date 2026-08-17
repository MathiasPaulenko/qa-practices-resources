from shop_domain import Cart, DiscountEngine, Inventory, AlertService


def before_scenario(context, scenario):
    context.catalog = {}
    context.cart = Cart()
    context.discount_engine = DiscountEngine()
    context.inventory = Inventory()
    context.alert_service = AlertService(context.inventory)
    context.search_results = []
    context.results = None
    context.response = None
