# SBOM and Supply Chain Testing — Runnable Companion

Runnable snippets from the QAPractices guide
[SBOM and Supply Chain Testing](https://qapractices.com/documentation/sbom-supply-chain-testing/):
generate an SBOM with Syft, scan it with Grype, sign and attach it with Cosign,
and gate releases in GitHub Actions.

## Contents

| File | What it does |
|---|---|
| `scripts/generate-sbom.sh` | CycloneDX SBOM from a container image (`syft 1.5+`) |
| `scripts/scan-sbom.sh` | Vulnerability scan of the SBOM (`grype --fail-on critical`) |
| `scripts/sign-and-attach.sh` | Sign the image and attach the SBOM (`cosign 2.x`) |
| `scripts/drift-check.sh` | Diff component lists between two SBOMs |
| `.github/workflows/supply-chain.yml` | CI job: generate → scan → gate → upload SBOM artifact |

## Requirements

- `syft` ≥ 1.5, `grype` ≥ 0.79, `cosign` 2.x, `python3`, `bash`
- A container image to inspect (or adapt the scripts to scan a directory)

## Quick start

```bash
./scripts/generate-sbom.sh myapp:1.4.2
./scripts/scan-sbom.sh sbom.cdx.json
./scripts/sign-and-attach.sh myapp:1.4.2 sbom.cdx.json
./scripts/drift-check.sh sbom-old.cdx.json sbom.cdx.json
```

## Notes

- `myapp:1.4.2` is a placeholder — replace it with your image.
- `cosign.key`/`cosign.pub` are a local key pair (`cosign generate-key-pair`);
  keyless OIDC signing works too, see the guide.
- The CI workflow pushes no images; it only generates, scans and stores the SBOM.
