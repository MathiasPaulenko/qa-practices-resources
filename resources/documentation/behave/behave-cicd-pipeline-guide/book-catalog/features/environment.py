from catalog_service import Catalog


def before_scenario(context, scenario):
    context.catalog = Catalog()


def after_scenario(context, scenario):
    if hasattr(context, 'catalog'):
        context.catalog.books.clear()
