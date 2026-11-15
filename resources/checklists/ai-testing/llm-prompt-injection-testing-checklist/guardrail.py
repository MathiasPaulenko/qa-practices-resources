"""Output guardrail check used by the checklist."""


def assert_no_disclosure(response, forbidden_terms, max_chars=200):
    """Raise AssertionError if a forbidden term appears in the response."""
    lower = response.lower()
    for term in forbidden_terms:
        if term in lower:
            raise AssertionError(f"Disclosure detected: {response[:max_chars]}")
    return True
