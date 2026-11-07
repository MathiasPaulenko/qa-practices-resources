# Caso de Estudio de Pruebas de Seguridad: SecureBank — Configs del Pipeline

Archivos companion del artículo [Caso de Estudio de Pruebas de Seguridad: SecureBank](https://qapractices.com/es/documentation/security-testing-case-study/) ([English version](https://qapractices.com/documentation/security-testing-case-study/)).

Son las configuraciones que SecureBank integró en GitHub Actions durante 16 semanas: gates de SAST + SCA en cada pull request, DAST autenticado de noche contra staging y escaneo de secretos en cada commit — todo alimentando un único tracker de hallazgos con severidad, responsable y SLA.

## Qué incluye

| Archivo | Qué hace |
| --- | --- |
| `security-gates.yml` | Workflow de GitHub Actions: Semgrep 1.184 + Snyk + SonarQube en PRs, OWASP ZAP full scan nocturno. Copiar a `.github/workflows/` |
| `pre-commit-config.yaml` | Pre-commit hook de GitLeaks 8.28. Copiar a `.pre-commit-config.yaml` |
| `zap/securebank.context` | Plantilla de contexto de ZAP con auth JSON + sesión bearer — lo que hace al escaneo autenticado |
| `zap/rules.tsv` | Reglas de filtrado de alertas para `action-full-scan` (baja el ruido conocido, mantiene la señal real) |
| `findings-tracker.sample.json` | Esquema del tracker de hallazgos con `dedupKey`, SLAs por severidad (24h / 7d / 30d) y registros de ejemplo |

## Cómo usarlo

1. **Pre-commit (la ganancia más rápida, ~1 hora):** copiá `pre-commit-config.yaml` a `.pre-commit-config.yaml` y después `pipx install pre-commit && pre-commit install`.
2. **Gates de PR:** copiá `security-gates.yml` a `.github/workflows/`. Configurá los secrets del repo `SEMGREP_APP_TOKEN`, `SNYK_TOKEN`, `SONAR_TOKEN`, `SONAR_HOST_URL`.
3. **DAST nocturno:** apuntá `target` a tu URL de staging. Exportá un contexto real desde ZAP Desktop (Session → Context → Export) tras grabar un login, y usá `zap/securebank.context` como plantilla de referencia. Ajustá `zap/rules.tsv` a tu stack.
4. **Tracker:** adaptá `findings-tracker.sample.json` al tracker que uses — los campos clave son `severity`, `owner`, `slaHours` y `dedupKey`.

## Requisitos

- Runners de GitHub Actions (ubuntu-latest) o CI equivalente
- `pre-commit` + `pipx` para los hooks locales
- Archivo de contexto de OWASP ZAP exportado desde ZAP Desktop para el escaneo autenticado
- Cuentas de Snyk y Semgrep AppSec Platform para los jobs de SCA/SAST

## Notas

- `staging.securebank.internal` es el objetivo ficticio del caso de estudio — reemplazalo.
- El DAST autenticado es la diferencia entre ~20% y ~80% de cobertura; los escaneos sin autenticar no ven los problemas de control de acceso.
- Afiná las reglas de SAST antes de activar los gates de bloqueo, o la primera semana inunda a los desarrolladores de falsos positivos.
