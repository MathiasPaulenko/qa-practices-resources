# Checklist de Testing de Cloud Storage — Companion

Comprobaciones ejecutables para el [Checklist de Testing de Cloud Storage (S3/Azure Blob)](https://qapractices.com/es/checklists/cloud-storage-testing-checklist).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `deny-insecure-transport-policy.json` | Declaración de bucket policy S3 que deniega cualquier petición sin `aws:SecureTransport` |
| `storage_checks.py` | Prueba de round-trip con boto3: sube un objeto, verifica el cifrado server-side, lo descarga y lo elimina |
| `azure_blob_checks.sh` | Auditoría con Azure CLI: verifica que `allowBlobPublicAccess` está deshabilitado y enumera un contenedor con auth por identidad |

## Uso

```bash
# Adjunta la declaración solo-HTTPS a la política del bucket
aws s3api put-bucket-policy --bucket my-app-bucket \
  --policy file://deny-insecure-transport-policy.json

# Ejecuta la prueba de round-trip + cifrado en S3 (requiere credenciales AWS)
python storage_checks.py

# Audita el acceso anónimo en una storage account de Azure
./azure_blob_checks.sh mystorageacct mycontainer
```

## Requisitos

- Python 3.10+ con `boto3` 1.34+
- Credenciales AWS con `s3:PutObject`, `s3:GetObject`, `s3:DeleteObject`, `s3:PutBucketPolicy` sobre el bucket de prueba
- Azure CLI 2.60+ con una identidad que tenga Storage Blob Data Reader en la cuenta
- Ejecuta todo contra una cuenta de staging, nunca contra producción

## Recurso Relacionado

- [Checklist de Testing de Cloud Storage (S3/Azure Blob)](https://qapractices.com/es/checklists/cloud-storage-testing-checklist)
- [Cloud Storage Testing Checklist](https://qapractices.com/checklists/cloud-storage-testing-checklist)
