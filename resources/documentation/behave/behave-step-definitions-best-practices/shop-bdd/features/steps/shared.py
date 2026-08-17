import parse
from behave import register_type


@parse.with_pattern(r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?')
def parse_money(text: str) -> int:
    return int(round(float(text.replace('$', '').replace(',', '')) * 100))


@parse.with_pattern(r'\d+%')
def parse_percentage(text: str) -> int:
    return int(text.replace('%', ''))


@parse.with_pattern(r'available|unavailable')
def parse_availability(text: str) -> bool:
    return text == 'available'


register_type(
    Money=parse_money,
    Percentage=parse_percentage,
    Availability=parse_availability,
)
