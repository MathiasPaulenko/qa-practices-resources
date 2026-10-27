"""Environment hooks for the smoke suite.

before_all sets a flag that TC-004 asserts; keep this file minimal —
real fixtures (database, API clients) belong in the regression suite.
"""


def before_all(context):
    context.global_flag = True
