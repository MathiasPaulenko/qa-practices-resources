#!/usr/bin/env bash
# Digital signature verification — OpenSSL 3.x commands
# Maps to the test cases in the Digital Signature Verification Test Cases resource.
set -euo pipefail

DOC="DOC-3001.pdf"

# --- Key generation (test fixtures) --------------------------------------
# TC-001 RSA-2048
openssl genrsa -out rsa-2048.pem 2048
openssl rsa -in rsa-2048.pem -pubout -out rsa-2048.pub

# TC-002 ECDSA P-256
openssl ecparam -name prime256v1 -genkey -noout -out ec-p256.pem
openssl ec -in ec-p256.pem -pubout -out ec-p256.pub

# TC-003 Ed25519 (RFC 8032)
openssl genpkey -algorithm ed25519 -out ed25519.pem
openssl pkey -in ed25519.pem -pubout -out ed25519.pub

# --- Sign + verify round-trip --------------------------------------------
# TC-001: sign with RSASSA-PKCS1-v1_5 SHA-256, verify with the public key
openssl dgst -sha256 -sign rsa-2048.pem -out DOC-3001.sig "$DOC"
openssl dgst -sha256 -verify rsa-2048.pub -signature DOC-3001.sig "$DOC"
# Expected: "Verified OK"

# TC-002: same flow with the ECDSA key — note the ~70-byte signature
openssl dgst -sha256 -sign ec-p256.pem -out DOC-3001-ec.sig "$DOC"
openssl dgst -sha256 -verify ec-p256.pub -signature DOC-3001-ec.sig "$DOC"
wc -c DOC-3001-ec.sig

# TC-003: Ed25519 is deterministic — sign twice, compare bytes
openssl pkeyutl -sign -inkey ed25519.pem -rawin -in "$DOC" -out ed-1.sig
openssl pkeyutl -sign -inkey ed25519.pem -rawin -in "$DOC" -out ed-2.sig
cmp ed-1.sig ed-2.sig && echo "deterministic"
openssl pkeyutl -verify -pubin -inkey ed25519.pub -rawin -in "$DOC" -sigfile ed-1.sig

# --- Negative cases -------------------------------------------------------
# TC-011: flip one byte in the signed document — must fail
cp "$DOC" DOC-3001-tampered.pdf
printf '\x00' | dd of=DOC-3001-tampered.pdf bs=1 seek=1024 conv=notrunc
if openssl dgst -sha256 -verify rsa-2048.pub -signature DOC-3001.sig DOC-3001-tampered.pdf; then
  echo "FAIL: tampered document verified"
  exit 1
else
  echo "PASS: tamper detected (Verification failure)"
fi

# TC-012: verify with the wrong public key — must fail
openssl dgst -sha256 -verify ec-p256.pub -signature DOC-3001.sig "$DOC" \
  && echo "FAIL: wrong key accepted" || echo "PASS: key mismatch rejected"

# --- Certificates ----------------------------------------------------------
# TC-006: chain validation root -> intermediate -> end-entity
# openssl verify -CAfile root-ca.pem -untrusted int-ca.pem cert-001.pem

# TC-013: expired certificate
# openssl verify -CAfile root-ca.pem expired-cert.pem   # -> error 10: certificate has expired

# TC-014: revocation via OCSP
# openssl ocsp -issuer int-ca.pem -cert cert-001.pem -url http://localhost:2560 -resp_text

# TC-004: detached CMS signature
# openssl cms -verify -in document.p7s -content document.pdf -CAfile root-ca.pem -out /dev/null

# TC-007: RFC 3161 timestamp token
# openssl ts -verify -in DOC-3001.tsr -data DOC-3001.pdf -CAfile tsa-chain.pem
