"""Example tests tagged with risk markers for the RBT CI pipeline."""
import pytest


@pytest.mark.critical
def test_checkout_completes_purchase():
    """Payment processing fails = Critical risk (score 20)."""
    assert True


@pytest.mark.critical
def test_refund_flow_returns_funds():
    assert True


@pytest.mark.high
def test_search_returns_relevant_results():
    """Updated product search = High risk (score 12)."""
    assert True


@pytest.mark.medium
def test_wishlist_persists_items():
    """Wishlist feature = Medium risk (score 9)."""
    assert True


@pytest.mark.low
def test_footer_links_render():
    """Footer links = Low risk (score 2)."""
    assert True
