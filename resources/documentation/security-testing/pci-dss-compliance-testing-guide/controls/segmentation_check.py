"""Segmentation check — verifies an out-of-scope segment cannot reach the CDE.

Requirement 11.4.5 (PCI DSS v4.0): penetration-testing segmentation
controls to prove isolation actually holds. Run this from a host in the
segment you claim is out of scope, targeting every CDE system. Any
reachable port invalidates the segmentation claim.
"""

import socket
import sys
from concurrent.futures import ThreadPoolExecutor

DEFAULT_PORTS = [22, 80, 443, 1433, 1521, 3306, 3389, 5432, 5985, 6379, 8080, 8443, 9200, 27017]


def port_open(host: str, port: int, timeout: float = 2.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def check_segmentation(host: str, ports: list[int] | None = None) -> list[int]:
    """Return the list of reachable ports on host — must be empty."""
    ports = ports or DEFAULT_PORTS
    with ThreadPoolExecutor(max_workers=32) as pool:
        results = pool.map(lambda p: port_open(host, p), ports)
    return [p for p, open_ in zip(ports, results) if open_]


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python -m controls.segmentation_check <cde-host> [port ...]")
        return 2
    host = sys.argv[1]
    ports = [int(p) for p in sys.argv[2:]] or None
    reachable = check_segmentation(host, ports)
    if reachable:
        print(f"FAIL: {host} reachable on {len(reachable)} port(s): {reachable}")
        print("Segmentation claim INVALID — this segment is in CDE scope")
        return 1
    print(f"PASS: {host} unreachable on all probed ports — segment stays out of scope")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
