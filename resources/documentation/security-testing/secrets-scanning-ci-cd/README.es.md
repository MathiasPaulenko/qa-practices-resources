# Escaneo de Secretos en CI/CD — Recursos complementarios

Configuraciones ejecutables de la guía [Escaneo de Secretos en CI/CD](https://qapractices.com/es/documentation/secrets-scanning-ci-cd/) de QAPractices.

## Qué incluye

| Ruta | Qué es |
|---|---|
| `.pre-commit-config.yaml` | Hook pre-commit de GitLeaks 8.30 — bloquea secretos antes de que entren al historial de Git |
| `.github/workflows/secrets.yml` | Escaneo de GitLeaks en cada PR y push, con `fetch-depth: 0` para historial completo |
| `.github/workflows/secret-scanning-pipeline.yml` | Escaneo TruffleHog con resultados verificados + escaneo de secretos en imágenes con Trivy, falla ante hallazgos |
| `scripts/check-unmasked-secrets.sh` | Comprobación con grep de credenciales sin enmascarar impresas en logs del pipeline |

## Inicio rápido

```bash
# 1. Puerta local: copia la config de pre-commit a la raíz de tu repo
cp .pre-commit-config.yaml /ruta/a/tu/repo/
pip install pre-commit
pre-commit install

# 2. Puertas de CI: copia los workflows
cp .github/workflows/*.yml /ruta/a/tu/repo/.github/workflows/

# 3. Escaneos puntuales
gitleaks detect --source . --verbose \
  --report-format json --report-path gitleaks-report.json
trufflehog git file://. --results=verified,unknown --json > trufflehog-report.json
trivy image app:scan --scanners secret --exit-code 1
```

## Reglas de la casa

- `GITLEAKS_LICENSE` solo hace falta para cuentas de organización en `gitleaks-action`; en repos personales puedes quitar esa línea de env.
- `fetch-depth: 0` no es negociable para escaneos de historial — un clon superficial no escanea nada que importe.
- TruffleHog corre con `--results=verified,unknown` para que las credenciales vivas salten primero; revisa los hallazgos `unknown` a mano antes de descartarlos.
- Rota primero, discute la reescritura del historial después. Un secreto eliminado que ya fue publicado sigue siendo un secreto filtrado.
- Documenta cada supresión con una razón y una fecha de revisión.

Guía: <https://qapractices.com/es/documentation/secrets-scanning-ci-cd/>
