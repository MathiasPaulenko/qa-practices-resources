# Testing de APIs gRPC — Scripts Companion

Companion de la guía [Cómo Probar APIs gRPC](https://qapractices.com/es/documentation/grpc-api-testing/). Comandos grpcurl ejecutables, configuración de `buf` para breaking changes y un test mock in-process de gRPC mínimo, todo contra el servicio ficticio de ledger `payflow` usado en la guía.

## Contenido

```text
scripts/
├── payflow.proto          # TransferService + AccountService de los ejemplos
├── buf.yaml               # config buf v2 (lint + breaking contra main)
├── grpcurl-commands.sh    # ejemplos list / describe / invoke / watch-stream
└── in_process_test.py     # test con servidor in-process (unary + cancelación)
```

## Requisitos

- grpcurl 1.9+
- buf CLI 1.x
- Python 3.12+ con `grpcio` 1.60+ y `grpcio-tools` (solo para `in_process_test.py`)

## Inicio rápido

```bash
# check de breaking changes contra main
cd scripts && buf breaking --against '.git#branch=main'

# generar stubs de Python y correr el test in-process
cd scripts
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. payflow.proto
pip install grpcio==1.60.0 pytest
python in_process_test.py
```

Si corres un servidor real con reflection habilitada en `localhost:50051`, los
ejemplos de `grpcurl-commands.sh` funcionan sin stubs generados.

## Notas

- El servicio `payflow` es ficticio; nada de esto habla con un backend real.
- `grpcurl-commands.sh` usa `-plaintext` para testing local. Para TLS mira el
  FAQ de TLS de la guía y quita el flag cuando configures certificados.
- `in_process_test.py` levanta el servidor en el mismo proceso, el patrón
  recomendado en la guía para tests de gRPC a nivel unitario.
