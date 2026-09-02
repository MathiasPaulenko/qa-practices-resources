# Container Security Testing Checklist — Companion

Scripts and Kubernetes policies for the [Container Security Testing Checklist](https://qapractices.com/checklists/container-security-testing-checklist).

## Files

| File | Purpose |
|------|---------|
| `scan-image.sh` | Scan a container image with Trivy 0.74.0 for HIGH and CRITICAL CVEs |
| `verify-signature.sh` | Verify a container image signature with Cosign 2.6.5 |
| `check-rbac.sh` | Audit Kubernetes RBAC permissions for a service account |
| `network-policy.yaml` | Default-deny egress + allow-list NetworkPolicy for Kubernetes |

## Usage

```bash
# Scan an image for vulnerabilities
./scan-image.sh myapp:1.2.3

# Verify image signature
./verify-signature.sh registry.example.com/myapp:1.2.3 cosign.pub

# Audit RBAC for a service account
./check-rbac.sh payments api-sa

# Apply network policies
kubectl apply -f network-policy.yaml
```

## Requirements

- Trivy 0.74.0+
- Cosign 2.6.5+
- kubectl (configured for your cluster)
- bash 4+

## Related Resource

- [Container Security Testing Checklist](https://qapractices.com/checklists/container-security-testing-checklist)
- [45 Container Security Testing Items: Docker & K8s](https://qapractices.com/checklists/container-security-testing-checklist)
