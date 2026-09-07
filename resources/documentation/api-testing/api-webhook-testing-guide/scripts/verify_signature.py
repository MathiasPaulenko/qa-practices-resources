"""Verify webhook signature using HMAC-SHA256 over raw body.

Usage:
    python verify_signature.py

Tests:
1. Valid signature matches
2. Tampered body fails
3. Wrong secret fails
4. Empty body edge case
"""

import hmac
import hashlib
import json
import sys


def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify HMAC-SHA256 signature over raw bytes using constant-time comparison."""
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


def test_valid_signature():
    secret = "whsec_test123"
    body = b'{"id":"evt_001","type":"payment_intent.succeeded","amount":5000}'
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    assert verify_signature(body, expected, secret), "Valid signature should match"
    print("PASS: valid signature matches")


def test_tampered_body():
    secret = "whsec_test123"
    body = b'{"id":"evt_001","type":"payment_intent.succeeded","amount":5000}'
    original_sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    tampered = b'{"id":"evt_001","type":"payment_intent.succeeded","amount":9999}'
    assert not verify_signature(tampered, original_sig, secret), "Tampered body should fail"
    print("PASS: tampered body rejected")


def test_wrong_secret():
    secret = "whsec_test123"
    wrong = "whsec_wrong"
    body = b'{"id":"evt_001","type":"payment_intent.succeeded"}'
    sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    assert not verify_signature(body, sig, wrong), "Wrong secret should fail"
    print("PASS: wrong secret rejected")


def test_empty_body():
    secret = "whsec_test123"
    body = b''
    sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    assert verify_signature(body, sig, secret), "Empty body with valid sig should match"
    print("PASS: empty body edge case handled")


def test_parsed_json_breaks():
    """Demonstrates why you must verify over raw bytes, not parsed JSON."""
    secret = "whsec_test123"
    raw = b'{"id":"evt_001","amount":5000}'
    parsed = json.dumps(json.loads(raw)).encode()
    sig_raw = hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()
    sig_parsed = hmac.new(secret.encode(), parsed, hashlib.sha256).hexdigest()
    assert sig_raw != sig_parsed, "Raw and parsed signatures should differ"
    print("PASS: raw vs parsed JSON produces different signatures (verify over raw!)")


if __name__ == "__main__":
    test_valid_signature()
    test_tampered_body()
    test_wrong_secret()
    test_empty_body()
    test_parsed_json_breaks()
    print("\nAll signature verification tests passed.")
