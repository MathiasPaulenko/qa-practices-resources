# Digital Signature Verification Test Cases — Companion

Runnable materials for the [Digital Signature Verification Test Cases](https://qapractices.com/test-cases/digital-signature-verification-test-cases/) resource on QAPractices.

## Contents

| File | What it is |
|---|---|
| `openssl-verify.sh` | OpenSSL 3.x commands for the suite: key generation (RSA-2048, ECDSA P-256, Ed25519), sign+verify round-trips, the byte-flip tamper case, the wrong-key case, and commented recipes for chain validation, OCSP, detached CMS signatures and RFC 3161 timestamps. |
| `tamper-detection-test.py` | pytest suite (pytest ≥8.3 + `cryptography` ≥43) covering TC-011 tamper detection, TC-012 wrong key, TC-015 corrupted signature, TC-016 empty document, TC-003 Ed25519 determinism and TC-025 curve mismatch. |

## Quick start

```bash
# OpenSSL flow (requires OpenSSL 3.x)
bash openssl-verify.sh

# Python suite
pip install pytest "cryptography>=43"
pytest tamper-detection-test.py -v
```

## Notes

- The API examples in the resource use the fictional SignVerify platform (`api.signverify.io/v1`) — treat the curl calls as request/response contracts for your own service, not a live endpoint.
- TC-006, TC-013, TC-014 and TC-007 in the shell file are commented because they need a certificate fixture chain (root CA → intermediate → end-entity, CRL, TSA token). Generate them with `openssl req`/`openssl ca` or reuse your PKI lab fixtures.
