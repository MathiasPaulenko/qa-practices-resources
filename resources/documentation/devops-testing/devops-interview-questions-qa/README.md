# Top 20 DevOps Interview Questions — Companion

Runnable versions of every config file shown in the guide
[Top 20 DevOps Interview Questions](https://qapractices.com/documentation/devops-interview-questions-qa).

## Files

| File | Question | What it does |
|---|---|---|
| `ci-pipeline.yml` | Q3 | GitHub Actions workflow: unit → integration → e2e with an 80% coverage gate |
| `compose.test.yml` | Q5 | Compose v2 test stack (app + Postgres tmpfs + Redis), exits with the test code |
| `Dockerfile.test` | Q4 | Minimal `node:20-alpine` test image |
| `k8s-regression-job.yaml` | Q7 | Kubernetes `batch/v1` Job, `parallelism: 3`, `restartPolicy: Never` |
| `retry-flaky.sh` | Q15 | Bash retry loop for flaky suites — 3 attempts, DB reset between them |
| `terraform/main.tf` | Q8 | Disposable `t3.medium` test-runner instance (AMI placeholder) |
| `terratest/infra_test.go` | Q9 | Terratest: deploy → assert `instance_ip` → destroy |

## Usage

```bash
# Compose test stack (Compose v2 — 'docker compose', no hyphen)
docker compose -f compose.test.yml up --abort-on-container-exit --exit-code-from app

# Kubernetes Job
kubectl apply -f k8s-regression-job.yaml && kubectl logs -f job/regression-tests

# Retry loop
bash retry-flaky.sh

# Terraform + Terratest (needs AWS creds, terraform ≥ 1.5, go ≥ 1.21)
cd terraform && terraform init && terraform plan
go test -v ./terratest/ -timeout 30m
```

Notes:

- `k8s-regression-job.yaml` uses `https://staging-api.example.com` as a placeholder — replace with your staging API.
- `terraform/main.tf` ships the AWS-docs example AMI; AMIs are region-specific — resolve yours with `aws ec2 describe-images` or an `aws_ami` data source.
- The compose file intentionally has **no `version:` key** — Compose v2/v5 ignores it and warns that it is obsolete.
