#!/usr/bin/env bash
# Sign an image and attach its SBOM with Cosign, then verify.
# Usage: ./sign-and-attach.sh <image:tag> [sbom-file]
set -euo pipefail
IMAGE="${1:?image tag required}"
SBOM="${2:-sbom.cdx.json}"
cosign sign --key cosign.key "$IMAGE"
cosign attach sbom --sbom "$SBOM" "$IMAGE"
cosign verify --key cosign.pub "$IMAGE"
