"""TLS configuration check — verifies the guarantees requirement 4 asks for.

Splits the network probe (probe_tls) from the evaluation logic
(evaluate_tls) so the pass/fail rules can be unit-tested without a
live endpoint. Minimum accepted version is TLS 1.2.
"""

import socket
import ssl
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone

MIN_TLS = (1, 2)  # TLS 1.2


@dataclass
class TlsResult:
    host: str
    port: int
    negotiated: str | None = None
    cipher: str | None = None
    cert_expires: str | None = None
    error: str | None = None
    failures: list[str] = field(default_factory=list)


def probe_tls(host: str, port: int = 443, timeout: float = 5.0) -> TlsResult:
    ctx = ssl.create_default_context()
    ctx.minimum_version = ssl.TLSVersion.TLSv1  # probe: accept weak so we can report it
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    result = TlsResult(host=host, port=port)
    try:
        with socket.create_connection((host, port), timeout=timeout) as raw:
            with ctx.wrap_socket(raw, server_hostname=host) as conn:
                result.negotiated = conn.version()
                result.cipher = conn.cipher()[0] if conn.cipher() else None
                cert = conn.getpeercert(binary_form=True)
                result.cert_expires = str(len(cert))  # presence only; expiry needs CERT_REQUIRED
    except (OSError, ssl.SSLError) as exc:
        result.error = str(exc)
    return result


def evaluate_tls(result: TlsResult) -> TlsResult:
    """Apply requirement-4 rules to a probe result. Pure logic — unit-testable."""
    if result.error:
        result.failures.append(f"connection failed: {result.error}")
        return result
    weak_versions = {"TLSv1", "TLSv1.1", "SSLv3", "SSLv2"}
    if result.negotiated in weak_versions:
        result.failures.append(f"weak protocol negotiated: {result.negotiated}")
    weak_ciphers = ("RC4", "DES", "3DES", "MD5", "NULL", "EXPORT", "anon")
    if result.cipher and any(w in result.cipher.upper() for w in weak_ciphers):
        result.failures.append(f"weak cipher negotiated: {result.cipher}")
    if not result.negotiated:
        result.failures.append("no TLS version negotiated")
    return result


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python -m controls.tls_check <host> [port]")
        return 2
    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 443
    result = evaluate_tls(probe_tls(host, port))
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"[{ts}] {host}:{port} negotiated={result.negotiated} cipher={result.cipher}")
    if result.failures:
        for f in result.failures:
            print(f"FAIL: {f}")
        return 1
    print("PASS: TLS configuration meets requirement 4 baseline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
