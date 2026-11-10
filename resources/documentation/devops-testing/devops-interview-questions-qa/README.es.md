# Top 20 Preguntas de Entrevista de DevOps — Companion

Versiones ejecutables de cada archivo de configuración de la guía
[Top 20 Preguntas de Entrevista de DevOps](https://qapractices.com/es/documentation/devops-interview-questions-qa).

## Archivos

| Archivo | Pregunta | Qué hace |
|---|---|---|
| `ci-pipeline.yml` | Q3 | Workflow de GitHub Actions: unit → integration → e2e con gate de cobertura al 80% |
| `compose.test.yml` | Q5 | Stack de prueba Compose v2 (app + Postgres con tmpfs + Redis), sale con el código del test |
| `Dockerfile.test` | Q4 | Imagen de test mínima `node:20-alpine` |
| `k8s-regression-job.yaml` | Q7 | Job de Kubernetes `batch/v1`, `parallelism: 3`, `restartPolicy: Never` |
| `retry-flaky.sh` | Q15 | Loop de reintento en bash para suites flaky — 3 intentos, con reset de DB entre ellos |
| `terraform/main.tf` | Q8 | Instancia `t3.medium` de test-runner desechable (AMI placeholder) |
| `terratest/infra_test.go` | Q9 | Terratest: desplegar → verificar `instance_ip` → destruir |

## Uso

```bash
# Stack de prueba Compose (Compose v2 — 'docker compose', sin guion)
docker compose -f compose.test.yml up --abort-on-container-exit --exit-code-from app

# Job de Kubernetes
kubectl apply -f k8s-regression-job.yaml && kubectl logs -f job/regression-tests

# Loop de reintento
bash retry-flaky.sh

# Terraform + Terratest (requiere credenciales AWS, terraform ≥ 1.5, go ≥ 1.21)
cd terraform && terraform init && terraform plan
go test -v ./terratest/ -timeout 30m
```

Notas:

- `k8s-regression-job.yaml` usa `https://staging-api.example.com` como placeholder — reemplazalo por tu API de staging.
- `terraform/main.tf` trae el AMI de ejemplo de los docs de AWS; los AMI son específicos por región — resolvé el tuyo con `aws ec2 describe-images` o un data source `aws_ami`.
- El archivo compose **no tiene clave `version:`** a propósito — Compose v2/v5 la ignora y emite un warning de obsoleta.
