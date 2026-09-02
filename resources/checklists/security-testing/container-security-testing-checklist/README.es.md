# Checklist de Seguridad de Contenedores — Companion

Scripts y políticas de Kubernetes para la [Checklist de Seguridad de Contenedores](https://qapractices.com/es/checklists/container-security-testing-checklist).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `scan-image.sh` | Escanear una imagen con Trivy 0.74.0 buscando CVEs HIGH y CRITICAL |
| `verify-signature.sh` | Verificar la firma de una imagen con Cosign 2.6.5 |
| `check-rbac.sh` | Auditar permisos RBAC de Kubernetes para un service account |
| `network-policy.yaml` | NetworkPolicy de default-deny egress + allow-list para Kubernetes |

## Uso

```bash
# Escanear una imagen en busca de vulnerabilidades
./scan-image.sh myapp:1.2.3

# Verificar la firma de una imagen
./verify-signature.sh registry.example.com/myapp:1.2.3 cosign.pub

# Auditar RBAC de un service account
./check-rbac.sh payments api-sa

# Aplicar las network policies
kubectl apply -f network-policy.yaml
```

## Requisitos

- Trivy 0.74.0+
- Cosign 2.6.5+
- kubectl (configurado para tu cluster)
- bash 4+

## Recurso relacionado

- [Checklist de Seguridad de Contenedores](https://qapractices.com/es/checklists/container-security-testing-checklist)
- [45 Items de Seguridad de Contenedores: Docker y K8s](https://qapractices.com/es/checklists/container-security-testing-checklist)
