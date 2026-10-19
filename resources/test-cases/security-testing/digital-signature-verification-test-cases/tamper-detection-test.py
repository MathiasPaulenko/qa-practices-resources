"""Tamper detection — pytest suite.

Covers TC-011 (tampered document), TC-012 (wrong public key),
TC-015 (corrupted signature) and TC-016 (empty document) from the
Digital Signature Verification Test Cases resource.

Requires: pytest>=8.3, cryptography>=43

    pip install pytest cryptography
    pytest tamper-detection-test.py -v
"""
import pytest
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, padding


@pytest.fixture(scope="module")
def ec_key():
    return ec.generate_private_key(ec.SECP256R1())


@pytest.fixture(scope="module")
def ed_key():
    return ed25519.Ed25519PrivateKey.generate()


def sign_ec(private_key, data: bytes) -> bytes:
    return private_key.sign(data, ec.ECDSA(hashes.SHA256()))


def verify_ec(public_key, signature: bytes, data: bytes) -> bool:
    try:
        public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        return False


def test_tampered_document_fails_verification(ec_key):
    """TC-011 — a single byte flip must invalidate the signature."""
    original = b"DOC-3001 vendor agreement content...".ljust(4096, b".")
    signature = sign_ec(ec_key, original)
    tampered = bytearray(original)
    tampered[1024] ^= 0xFF  # flip all bits of one byte mid-document
    assert verify_ec(ec_key.public_key(), signature, bytes(tampered)) is False


def test_wrong_public_key_fails_verification(ec_key):
    """TC-012 — a valid signature cannot be coerced to another key."""
    data = b"DOC-3001 vendor agreement content..."
    signature = sign_ec(ec_key, data)
    other = ec.generate_private_key(ec.SECP256R1())
    assert verify_ec(other.public_key(), signature, data) is False


def test_corrupted_signature_fails(ec_key):
    """TC-015 — corrupted signature bytes must fail, not crash."""
    data = b"DOC-3001 vendor agreement content..."
    signature = bytearray(sign_ec(ec_key, data))
    signature[10] ^= 0xFF
    assert verify_ec(ec_key.public_key(), bytes(signature), data) is False


def test_empty_document_signature_is_valid(ec_key):
    """TC-016 — signing a 0-byte payload is a valid edge case."""
    empty = b""
    signature = sign_ec(ec_key, empty)
    assert verify_ec(ec_key.public_key(), signature, empty) is True


def test_ed25519_signatures_are_deterministic(ed_key):
    """TC-003 — Ed25519 produces byte-identical signatures for the same input."""
    data = b"DOC-3001 vendor agreement content..."
    sig1 = ed_key.sign(data)
    sig2 = ed_key.sign(data)
    assert sig1 == sig2
    ed_key.public_key().verify(sig1, data)  # raises if invalid


def test_curve_mismatch_rejected():
    """TC-025 — a P-256 signature must not verify against a P-384 key."""
    p256 = ec.generate_private_key(ec.SECP256R1())
    p384 = ec.generate_private_key(ec.SECP384R1())
    data = b"DOC-3001 vendor agreement content..."
    signature = p256.sign(data, ec.ECDSA(hashes.SHA256()))
    with pytest.raises(InvalidSignature):
        p384.public_key().verify(signature, data, ec.ECDSA(hashes.SHA384()))
