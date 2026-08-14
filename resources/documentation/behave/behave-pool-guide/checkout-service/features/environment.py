from checkout_service import Cart, Inventory, PaymentGateway


def before_scenario(context, scenario):
    context.inventory = Inventory()
    context.cart = Cart()
    context.payment_gateway = PaymentGateway()
