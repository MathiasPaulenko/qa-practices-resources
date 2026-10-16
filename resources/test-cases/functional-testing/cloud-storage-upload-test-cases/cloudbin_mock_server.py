"""Runnable stdlib mock of the CloudBin multipart upload API.

    python cloudbin_mock_server.py [--port 8080]

Endpoints (all under http://127.0.0.1:{port}):

    POST /files/multipart                        {fileName, fileSize, folderId, chunkSize}
    PUT  /files/multipart/{uid}/chunks/{n}       raw chunk bytes
    GET  /files/multipart/{uid}/progress         progress JSON
    POST /files/multipart/{uid}/complete         {"chunks": [0, 1, ...]}
    GET  /files/{fileId}                         assembled file bytes
"""

import json
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from multipart_store import MultipartStore, UploadError

STORE = MultipartStore()

CHUNK_RE = re.compile(r"^/files/multipart/(UP-\w+)/chunks/(\d+)$")
UPLOAD_RE = re.compile(r"^/files/multipart/(UP-\w+)/(progress|complete)$")
FILE_RE = re.compile(r"^/files/(FILE-\w+)$")


class Handler(BaseHTTPRequestHandler):
    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self) -> bytes:
        return self.rfile.read(int(self.headers.get("Content-Length", 0)))

    def _fail(self, err: UploadError) -> None:
        self._json(err.status, {"error": err.message})

    def log_message(self, *args):  # keep the test output quiet
        pass

    def do_POST(self):
        if self.path == "/files/multipart":
            data = json.loads(self._body() or b"{}")
            try:
                self._json(201, STORE.initiate(
                    data["fileName"], data["fileSize"],
                    data.get("folderId", ""), data.get("chunkSize", 10485760)))
            except KeyError as e:
                self._json(400, {"error": f"missing field: {e}"})
            except UploadError as e:
                self._fail(e)
            return
        m = UPLOAD_RE.match(self.path)
        if m and m.group(2) == "complete":
            data = json.loads(self._body() or b"{}")
            try:
                self._json(200, STORE.complete(m.group(1), data.get("chunks")))
            except UploadError as e:
                self._fail(e)
            return
        self._json(404, {"error": "not found"})

    def do_PUT(self):
        m = CHUNK_RE.match(self.path)
        if not m:
            return self._json(404, {"error": "not found"})
        try:
            self._json(200, STORE.put_chunk(m.group(1), int(m.group(2)), self._body()))
        except UploadError as e:
            self._fail(e)

    def do_GET(self):
        m = UPLOAD_RE.match(self.path)
        if m and m.group(2) == "progress":
            try:
                return self._json(200, STORE.progress(m.group(1)))
            except UploadError as e:
                return self._fail(e)
        m = FILE_RE.match(self.path)
        if m:
            try:
                data = STORE.download(m.group(1))
            except UploadError as e:
                return self._fail(e)
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            return self.wfile.write(data)
        self._json(404, {"error": "not found"})


if __name__ == "__main__":
    port = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8080
    print(f"CloudBin mock listening on http://127.0.0.1:{port}")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
