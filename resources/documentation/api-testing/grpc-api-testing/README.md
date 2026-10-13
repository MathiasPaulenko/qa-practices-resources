# gRPC API Testing — Companion Scripts

Companion for the [How to Test gRPC APIs](https://qapractices.com/documentation/grpc-api-testing/) guide. Runnable grpcurl commands, a `buf` breaking-change setup and a minimal in-process gRPC mock test, all against the fictional `payflow` ledger service used in the guide.

## Contents

```text
scripts/
├── payflow.proto          # TransferService + AccountService used in the examples
├── buf.yaml               # buf v2 config (lint + breaking against main)
├── grpcurl-commands.sh    # list / describe / invoke / watch-stream examples
└── in_process_test.py     # grpcio in-process server test (unary + cancellation)
```

## Requirements

- grpcurl 1.9+
- buf CLI 1.x
- Python 3.12+ with `grpcio` 1.60+ and `grpcio-tools` (only for `in_process_test.py`)

## Quick start

```bash
# breaking-change check against main
cd scripts && buf breaking --against '.git#branch=main'

# generate Python stubs and run the in-process test
cd scripts
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. payflow.proto
pip install grpcio==1.60.0 pytest
python in_process_test.py
```

If you run a real server with reflection enabled on `localhost:50051`, the
`grpcurl-commands.sh` examples work without any generated stubs.

## Notes

- The `payflow` service is fictional; nothing here talks to a real backend.
- `grpcurl-commands.sh` uses `-plaintext` for local testing. For TLS see the
  guide's TLS FAQ and drop the flag once certificates are configured.
- `in_process_test.py` spins up the server in the same process, which is the
  pattern recommended in the guide for unit-level gRPC tests.
