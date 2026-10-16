"""In-memory model of the CloudBin multipart upload API from the article.

Mirrors the semantics exercised in the test cases: sessions expire,
chunks are deduplicated by ETag, progress comes from the server (not the
client), and a file only exists once ``/complete`` assembles it.
"""

import hashlib
import time
import uuid

DEFAULT_CHUNK_SIZE = 10 * 1024 * 1024  # 10 MB, same as the article
DEFAULT_QUOTA_BYTES = 15 * 1024 * 1024 * 1024  # 15 GB per account
BLOCKED_EXTENSIONS = {".exe", ".bat", ".com", ".scr", ".ps1"}
SESSION_TTL_SECONDS = 3600


class UploadError(Exception):
    """Domain error carrying the HTTP status the API would return."""

    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status
        self.message = message


def _ext(filename: str) -> str:
    dot = filename.rfind(".")
    return filename[dot:].lower() if dot >= 0 else ""


def _traversal(filename: str) -> bool:
    return ".." in filename or "/" in filename or "\\" in filename


class MultipartStore:
    """Quota-aware multipart session store shared by the HTTP wrapper and tests."""

    def __init__(self, quota_bytes: int = DEFAULT_QUOTA_BYTES):
        self.quota_bytes = quota_bytes
        self.used_bytes = 0
        self.sessions: dict[str, dict] = {}
        self.files: dict[str, dict] = {}

    # POST /files/multipart
    def initiate(self, file_name: str, file_size: int,
                 folder_id: str = "", chunk_size: int = DEFAULT_CHUNK_SIZE) -> dict:
        if _traversal(file_name):
            raise UploadError(422, f"filename rejected: {file_name!r}")
        if _ext(file_name) in BLOCKED_EXTENSIONS:
            raise UploadError(415, f"file type not allowed: {_ext(file_name)}")
        if file_size < 0:
            raise UploadError(400, "fileSize must be >= 0")
        if self.used_bytes + file_size > self.quota_bytes:
            raise UploadError(413, "quota exceeded")
        total = -(-file_size // chunk_size) if file_size else 0
        uid = f"UP-{uuid.uuid4().hex[:6].upper()}"
        self.sessions[uid] = {
            "uploadId": uid,
            "fileName": file_name,
            "fileSize": file_size,
            "folderId": folder_id,
            "chunkSize": chunk_size,
            "totalChunks": total,
            "expiresAt": time.time() + SESSION_TTL_SECONDS,
            "chunks": {},  # chunkNumber -> (etag, bytes)
            "completed": False,
        }
        return {
            "uploadId": uid,
            "fileName": file_name,
            "fileSize": file_size,
            "chunkSize": chunk_size,
            "totalChunks": total,
            "expiresAt": self.sessions[uid]["expiresAt"],
        }

    def _session(self, upload_id: str) -> dict:
        s = self.sessions.get(upload_id)
        if s is None:
            raise UploadError(404, "uploadId not found")
        if time.time() > s["expiresAt"]:
            raise UploadError(410, "upload session expired")
        return s

    # PUT /files/multipart/{uid}/chunks/{n}
    def put_chunk(self, upload_id: str, chunk_number: int, data: bytes) -> dict:
        s = self._session(upload_id)
        if s["completed"]:
            raise UploadError(409, "upload already completed")
        if chunk_number < 0 or chunk_number >= s["totalChunks"]:
            raise UploadError(400, f"chunkNumber out of range: {chunk_number}")
        etag = hashlib.md5(data).hexdigest()
        # Idempotent dedup: re-sending the same chunk is a no-op.
        existing = s["chunks"].get(chunk_number)
        if existing is not None and existing[0] == etag:
            return {"uploadId": upload_id, "chunkNumber": chunk_number,
                    "etag": etag, "size": len(data), "deduplicated": True}
        s["chunks"][chunk_number] = (etag, data)
        return {"uploadId": upload_id, "chunkNumber": chunk_number,
                "etag": etag, "size": len(data)}

    # GET /files/multipart/{uid}/progress
    def progress(self, upload_id: str) -> dict:
        s = self._session(upload_id)
        uploaded = len(s["chunks"])
        total = s["totalChunks"]
        pct = 100.0 if total == 0 else round(100.0 * uploaded / total, 1)
        return {
            "uploadId": upload_id,
            "totalChunks": total,
            "uploadedChunks": uploaded,
            "progress": min(pct, 100.0),  # never overshoots (edge case)
            "bytesUploaded": sum(len(d) for _, d in s["chunks"].values()),
            "bytesTotal": s["fileSize"],
            "status": "complete" if s["completed"] else "in_progress",
        }

    # POST /files/multipart/{uid}/complete
    def complete(self, upload_id: str, chunks: list[int] | None = None) -> dict:
        s = self._session(upload_id)
        if s["completed"]:
            raise UploadError(409, "upload already completed")
        expected = list(range(s["totalChunks"]))
        present = sorted(s["chunks"])
        if present != expected:
            missing = [n for n in expected if n not in s["chunks"]]
            raise UploadError(409, f"missing chunks: {missing[:5]}")
        if chunks is not None and sorted(chunks) != expected:
            raise UploadError(409, "declared chunk list does not match")
        payload = b"".join(s["chunks"][n][1] for n in expected)
        if len(payload) != s["fileSize"]:
            raise UploadError(409, "reassembled size mismatch")
        file_id = f"FILE-{uuid.uuid4().hex[:6].upper()}"
        s["completed"] = True
        self.used_bytes += len(payload)
        self.files[file_id] = {"fileName": s["fileName"], "data": payload,
                               "folderId": s["folderId"]}
        return {
            "fileId": file_id,
            "uploadId": upload_id,
            "fileName": s["fileName"],
            "size": len(payload),
            "md5": hashlib.md5(payload).hexdigest(),
            "status": "complete",
        }

    # GET /files/{file_id}
    def download(self, file_id: str) -> bytes:
        f = self.files.get(file_id)
        if f is None:
            raise UploadError(404, "file not found")
        return f["data"]
