# Testing de SBOM y Cadena de Suministro — Companion Ejecutable

Snippets ejecutables de la guía de QAPractices
[Testing de SBOM y Cadena de Suministro](https://qapractices.com/es/documentation/sbom-supply-chain-testing/):
genera un SBOM con Syft, escanéalo con Grype, fírmalo y adjúntalo con Cosign,
y bloquea releases en GitHub Actions.

## Contenido

| Archivo | Qué hace |
|---|---|
| `scripts/generate-sbom.sh` | SBOM CycloneDX desde una imagen de contenedor (`syft 1.5+`) |
| `scripts/scan-sbom.sh` | Escaneo de vulnerabilidades del SBOM (`grype --fail-on critical`) |
| `scripts/sign-and-attach.sh` | Firma la imagen y adjunta el SBOM (`cosign 2.x`) |
| `scripts/drift-check.sh` | Compara listas de componentes entre dos SBOMs |
| `.github/workflows/supply-chain.yml` | Job de CI: generar → escanear → gatear → subir el SBOM |

## Requisitos

- `syft` ≥ 1.5, `grype` ≥ 0.79, `cosign` 2.x, `python3`, `bash`
- Una imagen de contenedor para inspeccionar (o adapta los scripts a un directorio)

## Inicio rápido

```bash
./scripts/generate-sbom.sh myapp:1.4.2
./scripts/scan-sbom.sh sbom.cdx.json
./scripts/sign-and-attach.sh myapp:1.4.2 sbom.cdx.json
./scripts/drift-check.sh sbom-old.cdx.json sbom.cdx.json
```

## Notas

- `myapp:1.4.2` es un placeholder — reemplázalo por tu imagen.
- `cosign.key`/`cosign.pub` son un par de claves local (`cosign generate-key-pair`);
  la firma keyless por OIDC también funciona, ver la guía.
- El workflow de CI no publica imágenes; solo genera, escanea y guarda el SBOM.
