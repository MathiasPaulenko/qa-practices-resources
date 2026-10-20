"""Stdlib-only lab that mirrors TaskFlow's export/download behavior.

Models a minimal file-export service: deterministic zip creation, a manifest
with SHA-256 digests, HTTP range semantics (RFC 9110) and safety guards for
path traversal and decompression bombs. The pytest suite maps to the test
cases in https://qapractices.com/test-cases/file-compression-download-test-cases/
"""

import hashlib
import io
import posixpath
import zipfile


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_manifest(files: dict[str, bytes]) -> dict[str, str]:
    """name -> sha256 hex digest for every file in an export."""
    return {name: sha256_hex(content) for name, content in files.items()}


def create_zip(files: dict[str, bytes], comment: bytes = b"") -> bytes:
    """Build a deterministic zip archive in memory."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in sorted(files):
            zf.writestr(name, files[name])
        if comment:
            zf.comment = comment
    return buf.getvalue()


def zip_entries(zip_bytes: bytes) -> list[str]:
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        return zf.namelist()


def verify_archive(zip_bytes: bytes, manifest: dict[str, str]) -> None:
    """Raise AssertionError unless every entry matches its manifest digest."""
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        assert zf.testzip() is None, "archive fails CRC check"
        names = zf.namelist()
        assert len(names) == len(manifest), (
            f"entry count {len(names)} != manifest {len(manifest)}"
        )
        for name in names:
            assert name in manifest, f"unexpected entry {name!r}"
            data = zf.read(name)
            assert sha256_hex(data) == manifest[name], f"checksum mismatch: {name}"


def sanitize_entry(name: str) -> str:
    """Return a safe extraction path or raise ValueError on traversal."""
    if name.startswith("/") or name.startswith("\\") or ".." in name.split("/"):
        raise ValueError(f"unsafe zip entry: {name!r}")
    normalized = posixpath.normpath(name)
    if normalized.startswith("../"):
        raise ValueError(f"unsafe zip entry: {name!r}")
    return normalized


def check_unpacked_size(zip_bytes: bytes, max_unpacked: int) -> None:
    """Zip-bomb guard: reject archives whose declared unpacked size exceeds a cap."""
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        total = sum(info.file_size for info in zf.infolist())
    if total > max_unpacked:
        raise ValueError(f"archive unpacks to {total} bytes > cap {max_unpacked}")


def parse_range(range_header: str, size: int) -> tuple[int, int, int]:
    """Parse 'bytes=start-end' per RFC 9110.

    Returns (status, start, end) where status is 206 or 416 and end is inclusive.
    """
    if not range_header.startswith("bytes="):
        return 416, -1, -1
    spec = range_header[6:].split(",")[0].strip()
    try:
        start_s, _, end_s = spec.partition("-")
        if start_s == "":
            # suffix range: last N bytes
            suffix = int(end_s)
            if suffix <= 0:
                return 416, -1, -1
            return 206, max(0, size - suffix), size - 1
        start = int(start_s)
        end = int(end_s) if end_s else size - 1
    except ValueError:
        return 416, -1, -1
    if start >= size or start > end:
        return 416, -1, -1
    return 206, start, min(end, size - 1)


def serve_download(
    files: dict[str, bytes],
    file_id: str,
    owner: str,
    requester: str,
    range_header: str | None = None,
    download_name: str | None = None,
) -> tuple[int, dict, bytes]:
    """Simulate `GET /files/{id}/download` with auth, headers and range support.

    Returns (status, headers, body) exactly like the real endpoint should.
    """
    if file_id not in files:
        return 404, {"Content-Type": "application/json"}, b'{"error": "not found"}'
    if owner != requester:
        return 403, {"Content-Type": "application/json"}, b'{"error": "forbidden"}'

    payload = files[file_id]
    headers = {
        "Content-Type": "application/zip",
        "Accept-Ranges": "bytes",
        "Content-Disposition": f'attachment; filename="{download_name or file_id}.zip"',
    }
    if range_header:
        status, start, end = parse_range(range_header, len(payload))
        if status == 416:
            headers["Content-Range"] = f"bytes */{len(payload)}"
            return 416, headers, b""
        body = payload[start : end + 1]
        headers["Content-Range"] = f"bytes {start}-{end}/{len(payload)}"
        headers["Content-Length"] = str(len(body))
        return 206, headers, body

    headers["Content-Length"] = str(len(payload))
    return 200, headers, payload
