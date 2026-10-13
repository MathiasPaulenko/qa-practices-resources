"""In-process gRPC mock test for the payflow ledger service.

Runs a generic-handlers server in the same process, so the only dependency is
grpcio itself — no generated stubs needed. Mirrors the guide's recommendation
of in-process servers for unit-level gRPC tests.

Run:  pip install grpcio==1.60.0 && python in_process_test.py
"""

import json
import time
from concurrent.futures import ThreadPoolExecutor

import grpc


def _request_deserializer(payload: bytes) -> dict:
    return json.loads(payload.decode("utf-8"))


def _response_serializer(obj: dict) -> bytes:
    return json.dumps(obj).encode("utf-8")


class TransferServiceHandler:
    """Minimal mock: GetTransfer returns a settled transfer or INVALID_ARGUMENT."""

    def get_transfer(self, request, context):
        transfer_id = request.get("transfer_id")
        if not transfer_id:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "transfer_id is required")
        return {
            "transferId": transfer_id,
            "status": "STATUS_SETTLED",
            "amount": "1240.00",
            "currency": "USD",
        }

    def watch_transactions(self, request, context):
        for i in range(3):
            if not context.is_active():
                return
            yield {
                "transactionId": f"tx-{i}",
                "accountId": request.get("account_id", ""),
                "amount": "10.00",
                "direction": "CREDIT",
            }
            time.sleep(0.01)


def build_server() -> grpc.Server:
    handler = TransferServiceHandler()
    server = grpc.server(ThreadPoolExecutor(max_workers=4))
    generic = {
        "com.payflow.ledger.TransferService": {
            "GetTransfer": grpc.unary_unary_rpc_method_handler(
                handler.get_transfer, _request_deserializer, _response_serializer
            )
        },
        "com.payflow.ledger.AccountService": {
            "WatchTransactions": grpc.unary_stream_rpc_method_handler(
                handler.watch_transactions, _request_deserializer, _response_serializer
            )
        },
    }
    for service, methods in generic.items():
        server.add_generic_rpc_handlers(
            (grpc.method_handlers_generic_handler(service, methods),)
        )
    return server


def main() -> None:
    server = build_server()
    port = server.add_insecure_port("127.0.0.1:0")
    server.start()

    channel = grpc.insecure_channel(f"127.0.0.1:{port}")

    unary = channel.unary_unary(
        "/com.payflow.ledger.TransferService/GetTransfer",
        request_serializer=_response_serializer,
        response_deserializer=_request_deserializer,
    )

    resp = unary({"transfer_id": "txn-9f4c"})
    assert resp["status"] == "STATUS_SETTLED", resp
    print("unary happy path: OK ->", resp["transferId"])

    try:
        unary({})
        raise AssertionError("expected INVALID_ARGUMENT")
    except grpc.RpcError as err:
        assert err.code() == grpc.StatusCode.INVALID_ARGUMENT
        print("empty payload rejected: OK ->", err.code())

    stream = channel.unary_stream(
        "/com.payflow.ledger.AccountService/WatchTransactions",
        request_serializer=_response_serializer,
        response_deserializer=_request_deserializer,
    )
    call = stream({"account_id": "acc-7712"})
    first = next(iter(call))
    call.cancel()  # mid-stream cancellation, like Ctrl+C on grpcurl
    assert call.code() == grpc.StatusCode.CANCELLED
    print("stream + cancel: OK -> first message", first["transactionId"])

    server.stop(None)
    print("all checks passed")


if __name__ == "__main__":
    main()
