#!/usr/bin/env bash
# grpcurl examples against a local gRPC server with reflection enabled.
# These are the commands from the guide; they work against any server that
# exposes grpc.reflection on localhost:50051.

set -euo pipefail

HOST="${GRPC_HOST:-localhost:50051}"

# List all services exposed via reflection.
grpcurl -plaintext "$HOST" list

# Inspect the TransferService contract.
grpcurl -plaintext "$HOST" describe com.payflow.ledger.TransferService

# Unary call: fetch one transfer.
grpcurl -plaintext \
  -d '{"transfer_id": "txn-9f4c"}' \
  "$HOST" com.payflow.ledger.TransferService/GetTransfer

# Unary call with an empty payload — expect INVALID_ARGUMENT.
grpcurl -plaintext \
  -d '{}' \
  "$HOST" com.payflow.ledger.TransferService/GetTransfer || true

# Server-streaming call: watch transactions until you cancel (Ctrl+C).
grpcurl -plaintext \
  -d '{"account_id": "acc-7712"}' \
  "$HOST" com.payflow.ledger.AccountService/WatchTransactions
