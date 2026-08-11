from behave import register_type
from parse_type import TypeBuilder


parse_product = TypeBuilder.make_choice(['Book', 'Laptop', 'Mouse'])
register_type(Product=parse_product)
