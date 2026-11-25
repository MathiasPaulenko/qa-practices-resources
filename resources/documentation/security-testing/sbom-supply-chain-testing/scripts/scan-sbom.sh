#!/usr/bin/env bash
# Scan an SBOM for vulnerabilities with Grype; fails on critical CVEs.
# Usage: ./scan-sbom.sh [sbom-file]
set -euo pipefail
SBOM="${1:-sbom.cdx.json}"
grype "sbom:${SBOM}" --fail-on critical
