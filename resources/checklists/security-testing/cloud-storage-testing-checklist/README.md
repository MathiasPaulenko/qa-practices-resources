# Cloud Storage Testing Checklist — Companion

Runnable checks for the [Cloud Storage Testing Checklist (S3/Azure Blob)](https://qapractices.com/checklists/cloud-storage-testing-checklist).

## Files

| File | Purpose |
|------|---------|
| `deny-insecure-transport-policy.json` | S3 bucket policy statement that denies any request without `aws:SecureTransport` |
| `storage_checks.py` | boto3 round-trip test: uploads an object, asserts server-side encryption, downloads and deletes it |
| `azure_blob_checks.sh` | Azure CLI audit: verifies `allowBlobPublicAccess` is disabled and lists a container through identity auth |

## Usage

```bash
# Attach the HTTPS-only statement to a bucket policy
aws s3api put-bucket-policy --bucket my-app-bucket \
  --policy file://deny-insecure-transport-policy.json

# Run the S3 round-trip + encryption check (requires AWS credentials)
python storage_checks.py

# Audit anonymous access on an Azure storage account
./azure_blob_checks.sh mystorageacct mycontainer
```

## Requirements

- Python 3.10+ with `boto3` 1.34+
- AWS credentials with `s3:PutObject`, `s3:GetObject`, `s3:DeleteObject`, `s3:PutBucketPolicy` on the test bucket
- Azure CLI 2.60+ with an identity holding Storage Blob Data Reader on the account
- Run everything against a staging account, never production

## Related Resource

- [Cloud Storage Testing Checklist (S3/Azure Blob)](https://qapractices.com/checklists/cloud-storage-testing-checklist)
- [Checklist de Testing de Cloud Storage](https://qapractices.com/es/checklists/cloud-storage-testing-checklist)
