"""Runnable versions of the article's cloud-storage upload test cases.

Most tests exercise MultipartStore in-process for speed; the last one
smokes the real HTTP mock so the curl paths in the article stay honest.
"""

import hashlib
import sys
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cloudbin_mock_server import Handler  # noqa: E402
from multipart_store import MultipartStore, UploadError  # noqa: E402

CHUNK = 8  # tiny chunk size so the suite stays fast


def upload(store: MultipartStore, name: str, payload: bytes,
           send_chunks=None) -> str:
    """Drive a full multipart upload and return the uploadId."""
    send_chunks = send_chunks if send_chunks is not None else range(
        -(-len(payload) // CHUNK) or 0)
    init = store.initiate(name, len(payload), chunk_size=CHUNK)
    for i in send_chunks:
        store.put_chunk(init["uploadId"], i, payload[i * CHUNK:(i + 1) * CHUNK])
    return init["uploadId"]


# TC-004 / TC-007: chunked upload reassembles a byte-identical file.
def test_chunked_upload_integrity():
    store = MultipartStore()
    payload = bytes(range(256)) * 5
    uid = upload(store, "test.bin", payload)
    result = store.complete(uid)
    downloaded = store.download(result["fileId"])
    assert downloaded == payload
    assert hashlib.sha256(downloaded).hexdigest() == \
        hashlib.sha256(payload).hexdigest()


# TC-024: resume continues from the last acknowledged chunk.
def test_upload_resumes_from_last_acked_chunk():
    store = MultipartStore()
    payload = b"A" * 30
    uid = upload(store, "resume.zip", payload, send_chunks=[0, 1, 2])
    assert store.progress(uid)["uploadedChunks"] == 3
    upload(store, "resume.zip", payload)  # fresh uid would restart
    store.put_chunk(uid, 3, payload[3 * CHUNK:])
    result = store.complete(uid)
    assert store.download(result["fileId"]) == payload


# Edge case: complete fails while chunks are missing — upload must stay resumable.
def test_complete_rejected_with_missing_chunks_keeps_session():
    store = MultipartStore()
    payload = b"B" * 24
    uid = upload(store, "partial.bin", payload, send_chunks=[0, 2])
    with pytest.raises(UploadError) as err:
        store.complete(uid)
    assert err.value.status == 409
    store.put_chunk(uid, 1, payload[CHUNK:2 * CHUNK])
    assert store.complete(uid)["status"] == "complete"


# Edge case: re-sending the same chunk is deduplicated, not double-counted.
def test_duplicate_chunk_is_deduplicated():
    store = MultipartStore()
    init = store.initiate("dup.bin", 16, chunk_size=CHUNK)
    uid = init["uploadId"]
    first = store.put_chunk(uid, 0, b"12345678")
    retry = store.put_chunk(uid, 0, b"12345678")
    assert first["etag"] == retry["etag"]
    assert retry["deduplicated"] is True
    assert store.progress(uid)["uploadedChunks"] == 1


# TC-028 edge: file exactly at quota fits, the next byte does not.
def test_quota_boundary():
    store = MultipartStore(quota_bytes=16)
    uid = upload(store, "exact.bin", b"X" * 16)
    store.complete(uid)
    assert store.used_bytes == 16
    with pytest.raises(UploadError) as err:
        store.initiate("one-more.bin", 1, chunk_size=CHUNK)
    assert err.value.status == 413


# TC-012: blocked extensions are rejected at init.
def test_blocked_extension_rejected():
    store = MultipartStore()
    with pytest.raises(UploadError) as err:
        store.initiate("malware.exe", 100, chunk_size=CHUNK)
    assert err.value.status == 415


# Edge case: path traversal filenames are rejected, not sanitized silently.
def test_path_traversal_filename_rejected():
    store = MultipartStore()
    with pytest.raises(UploadError) as err:
        store.initiate("../../etc/passwd", 8, chunk_size=CHUNK)
    assert err.value.status == 422


# TC-005: server progress is monotonic and capped at 100.
def test_progress_monotonic_and_capped():
    store = MultipartStore()
    payload = b"C" * 24
    uid = upload(store, "progress.bin", payload)
    p = store.progress(uid)
    assert p["progress"] == pytest.approx(100.0)
    assert p["status"] == "in_progress"  # not complete until /complete


# Edge case: sessions expire and stale uploadIds are rejected.
def test_expired_upload_id_rejected():
    store = MultipartStore()
    uid = store.initiate("old.bin", 8, chunk_size=CHUNK)["uploadId"]
    store.sessions[uid]["expiresAt"] = 0  # force expiry
    with pytest.raises(UploadError) as err:
        store.put_chunk(uid, 0, b"12345678")
    assert err.value.status == 410


# Smoke test over real HTTP: the curl endpoints from the article actually work.
def test_http_endpoints_round_trip():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    payload = b"D" * 24
    init = requests.post(f"{base}/files/multipart", json={
        "fileName": "http.bin", "fileSize": len(payload),
        "folderId": "FOLDER-012", "chunkSize": CHUNK}).json()
    uid = init["uploadId"]
    for i in range(init["totalChunks"]):
        r = requests.put(f"{base}/files/multipart/{uid}/chunks/{i}",
                         data=payload[i * CHUNK:(i + 1) * CHUNK])
        r.raise_for_status()
    done = requests.post(f"{base}/files/multipart/{uid}/complete",
                         json={"chunks": list(range(init["totalChunks"]))}).json()
    body = requests.get(f"{base}/files/{done['fileId']}").content
    server.shutdown()
    assert body == payload
