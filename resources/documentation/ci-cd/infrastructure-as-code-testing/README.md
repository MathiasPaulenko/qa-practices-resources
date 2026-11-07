# Infrastructure as Code (IaC) Testing — Runnable Examples

Runnable versions of the examples in the [Infrastructure as Code (IaC) Testing Guide](https://qapractices.com/documentation/infrastructure-as-code-testing/).

## Contents

| Path | What it does |
|---|---|
| `policy/security.rego` | OPA/Rego policy evaluated against `terraform show -json` output: denies world-open SSH and unencrypted S3 buckets. |
| `tests/s3_bucket.tftest.hcl` | Native `terraform test` suite (Terraform 1.6+): plan assertion on bucket name + apply assertion on encryption. |
| `ci/iac-test.yml` | Three-job GitHub Actions gate: fmt/validate → Checkov scan with SARIF upload → plan artifact. |
| `scripts/drift-check.sh` | Cron-ready drift check using `terraform plan -detailed-exitcode`. |
| `config/.tflint.hcl` | tflint rules: unused declarations, snake_case naming, deprecated syntax. |

## Usage

```bash
# OPA policy check against a plan
terraform show -json tfplan > plan.json
opa eval --data policy/ --input plan.json "data.terraform.analysis.deny"

# Native test suite (place under your module's tests/)
terraform test

# Drift check (schedule it — drift happens between deploys)
bash scripts/drift-check.sh
```

## Notes

- `terraform validate` checks syntax only — a world-open security group validates fine. The security and policy layers exist for what syntax can't see.
- Integration tests create real resources and real bills; run them on merge or a schedule, not per-commit.
