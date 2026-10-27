"""Validate an Apple in-app purchase receipt server-side.

Usage:
    APPLE_SHARED_SECRET=... python apple_receipt_validation.py <receipt.b64>

Requires: requests 2.32+ — pip install requests
Related test cases: TC-MP-006, TC-MP-007, TC-MP-008
"""
import os
import sys

import requests

SANDBOX_URL = "https://sandbox.itunes.apple.com/verifyReceipt"
PROD_URL = "https://buy.itunes.apple.com/verifyReceipt"


def validate_apple_receipt(receipt_data: str, password: str, sandbox: bool = True):
    """Verify a receipt against Apple's verifyReceipt endpoint.

    Returns the list of in-app purchase records on success.
    Raises AssertionError for any non-zero Apple status code.
    """
    url = SANDBOX_URL if sandbox else PROD_URL
    response = requests.post(url, json={
        "receipt-data": receipt_data,
        "password": password,
    }, timeout=10)
    payload = response.json()
    # status 21007 means "this is a sandbox receipt sent to production":
    # retry against the sandbox endpoint — do not hardcode a single URL.
    if payload.get("status") == 21007 and not sandbox:
        return validate_apple_receipt(receipt_data, password, sandbox=True)
    status = payload.get("status", -1)
    assert status == 0, f"Invalid receipt, Apple status={status}"
    return payload["receipt"]["in_app"]


if __name__ == "__main__":
    receipt = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("RECEIPT_DATA")
    password = os.environ.get("APPLE_SHARED_SECRET")
    if not receipt or not password:
        sys.exit("Set RECEIPT_DATA and APPLE_SHARED_SECRET (or pass receipt as argv[1])")
    in_app = validate_apple_receipt(receipt, password)
    print(f"Valid receipt — {len(in_app)} in-app purchase record(s)")
    for p in in_app:
        print(f"  {p.get('product_id')} | transaction {p.get('transaction_id')}")
