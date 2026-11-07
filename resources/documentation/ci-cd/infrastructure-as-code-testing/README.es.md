# Testing de Infrastructure as Code (IaC) — Ejemplos ejecutables

Versiones ejecutables de los ejemplos de la [Guía de Testing de Infrastructure as Code (IaC)](https://qapractices.com/es/documentation/infrastructure-as-code-testing/).

## Contenido

| Ruta | Qué hace |
|---|---|
| `policy/security.rego` | Política OPA/Rego evaluada contra la salida de `terraform show -json`: deniega SSH abierto al mundo y buckets S3 sin encriptar. |
| `tests/s3_bucket.tftest.hcl` | Suite nativa de `terraform test` (Terraform 1.6+): assertion de plan sobre el nombre del bucket + assertion de apply sobre la encriptación. |
| `ci/iac-test.yml` | Gate de GitHub Actions en tres jobs: fmt/validate → scan Checkov con subida SARIF → artefacto de plan. |
| `scripts/drift-check.sh` | Chequeo de drift listo para cron usando `terraform plan -detailed-exitcode`. |
| `config/.tflint.hcl` | Reglas de tflint: declaraciones sin usar, naming snake_case, sintaxis deprecada. |

## Uso

```bash
# Chequeo de política OPA contra un plan
terraform show -json tfplan > plan.json
opa eval --data policy/ --input plan.json "data.terraform.analysis.deny"

# Suite nativa de tests (ubicarla en tests/ dentro de tu módulo)
terraform test

# Chequeo de drift (programalo — el drift pasa entre deploys)
bash scripts/drift-check.sh
```

## Notas

- `terraform validate` solo chequea sintaxis — un security group abierto al mundo valida sin problema. Las capas de seguridad y políticas existen para lo que la sintaxis no puede ver.
- Los tests de integración crean recursos reales y facturas reales; corrélos en merge o en un schedule, no por commit.
