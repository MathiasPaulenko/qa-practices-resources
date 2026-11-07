# Mejores Herramientas de Security Testing — Ejemplos de escaneo ejecutables

Versiones ejecutables de los tres ejemplos del artículo
[Mejores Herramientas de Security Testing (2026)](https://qapractices.com/es/documentation/best-security-testing-tools/).

## Contenido

| Archivo | Qué hace |
|---|---|
| `zap-baseline.sh` | Escaneo baseline de OWASP ZAP contra una aplicación en ejecución vía Docker (`ghcr.io/zaproxy/zaproxy:stable`, línea ZAP 2.15). Genera `zap-baseline.html`. |
| `nuclei-scan.sh` | Escaneo dirigido con Nuclei v3: templates de severidad critical/high, limitado a 10 req/s. |
| `github-actions/dependency-check.yml` | Job de GitHub Actions que ejecuta OWASP Dependency-Check contra el feed del NVD en cada push; rompe el build con CVSS ≥ 7 y sube el reporte HTML. |

## Uso

```bash
./zap-baseline.sh https://staging.example.com
./nuclei-scan.sh https://staging.example.com
```

Para el job de GitHub Actions, copiá `github-actions/dependency-check.yml` a
`.github/workflows/` en tu repositorio. El escaneo necesita una `NVD_API_KEY`
para descargas confiables del feed en runners ocupados: pedí una en
<https://nvd.nist.gov/developers/request-an-api-key> y agregala como variable
de entorno del step si aparece throttling.

## Requisitos

- Docker (para el script de ZAP baseline)
- Nuclei v3 — `go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest`
- Un repositorio de GitHub con Actions habilitado (para el workflow)

## Cómo elegir una herramienta

Estos scripts cubren las tres capas de mayor ROI del artículo: escaneo de
dependencias (Dependency-Check), DAST de runtime (baseline de ZAP) y escaneo
dirigido por templates (Nuclei). Se complementan entre sí — ninguno reemplaza
el penetration testing manual antes de los releases importantes.
