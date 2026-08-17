from behave import given, register_type
import parse


@parse.with_pattern(r'ORD-\d{4}-\d{5}')
def parse_order_ref(text: str) -> str:
    return text


register_type(OrderRef=parse_order_ref)


@given('the order {ref:OrderRef} is {status}')
def step_order_status(context, ref, status):
    context.order_ref = ref
    context.order_status = status
