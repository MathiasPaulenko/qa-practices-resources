#!/usr/bin/env bash
# Generate a CycloneDX SBOM for a container image with Syft.
# Usage: ./generate-sbom.sh <image:tag>
set -euo pipefail
IMAGE="${1:-myapp:latest}"
syft "$IMAGE" -o cyclonedx-json=sbom.cdx.json
echo "SBOM written to sbom.cdx.json"
