# Cloud Storage Upload Test Cases — Companion

Runnable mock of the CloudBin multipart upload API used in the article
[Cloud Storage Upload Test Cases](https://qapractices.com/test-cases/cloud-storage-upload-test-cases/):

- `multipart_store.py` — in-memory model of the multipart semantics
  exercised in the suite: session expiry, chunk deduplication by ETag,
  server-side progress, quota enforcement and `complete`-time assembly.
- `cloudbin_mock_server.py` — stdlib `http.server` wrapper exposing the
  same REST endpoints used in the curl examples (`POST /files/multipart`,
  `PUT /chunks/{n}`, `GET /progress`, `POST /complete`, `GET /files/{id}`).
- `tests/test_multipart_upload.py` — pytest suite covering chunked
  integrity, resume from the last acknowledged chunk, missing-chunk and
  duplicate-chunk edge cases, quota boundaries, blocked extensions, path
  traversal filenames, progress monotonicity and session expiry.

## Run

```bash
pip install -r requirements.txt
pytest tests/
```

To poke the API manually, run `python cloudbin_mock_server.py --port 8080`
and use the curl examples from the article against `http://127.0.0.1:8080`
instead of `https://api.cloudbin.io/v1`.

Covered test cases: TC-004/TC-005/TC-007 (chunked integrity and progress),
TC-012 (blocked extension), TC-024 (resume), TC-028 (quota boundary) and
the edge table (stale session, silent `complete` failure, duplicate chunk,
path traversal).
