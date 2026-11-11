#!/usr/bin/env bash
# Anonymous-access audit for an Azure storage account.
# Usage: ./azure_blob_checks.sh <storage-account> <container>
# Requires Azure CLI 2.60+ and an identity with Storage Blob Data Reader.
set -euo pipefail

ACCOUNT="${1:?storage account name required}"
CONTAINER="${2:?container name required}"

PUBLIC_ACCESS=$(az storage account show --name "$ACCOUNT" \
  --query allowBlobPublicAccess --output tsv)

if [ "$PUBLIC_ACCESS" != "false" ]; then
  echo "FAIL: allowBlobPublicAccess=$PUBLIC_ACCESS on $ACCOUNT (expected: false)"
  exit 1
fi
echo "OK: allowBlobPublicAccess=false on $ACCOUNT"

# Enumerate blobs through identity auth — confirms RBAC actually works.
az storage blob list --container-name "$CONTAINER" \
  --account-name "$ACCOUNT" --auth-mode login \
  --query "[].name" --output tsv
