import os
from cart.service import ProductCatalog, Cart
from api_server import start_server, stop_server


def before_all(context):
    context.api_server = start_server()


def before_scenario(context, scenario):
    context.catalog = ProductCatalog()
    context.cart = Cart()
    context.base_url = os.environ.get(
        'API_BASE_URL',
        context.config.userdata.get('api_url', 'http://127.0.0.1:8765')
    )
    context.token = os.environ.get('API_TOKEN')


def after_scenario(context, scenario):
    if hasattr(context, 'cart'):
        context.cart.clear()
    if hasattr(context, 'response'):
        context.response.close()


def after_all(context):
    if hasattr(context, 'api_server'):
        stop_server(context.api_server)
