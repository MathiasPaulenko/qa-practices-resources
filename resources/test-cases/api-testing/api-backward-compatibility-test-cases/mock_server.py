"""Mock TaskFlow API implementing the 2025-01 and 2026-07 contracts.

Versioning happens through the `API-Version` header:
  - `2025-01`  -> legacy contract (`assignee_id` flat field)
  - `2026-07`  -> current contract (`assignee` object + `story_points`)
  - `2024-03`  -> retired version, returns 410 Gone with a Link header
  - missing    -> defaults to `2025-01`
  - unknown    -> 400 listing supported versions

The 2026-07 contract dual-ships `assignee_id` alongside `assignee`
with a `Deprecation: true` header, matching TC-005.

Run standalone:  python mock_server.py 8571
"""
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

SUPPORTED = ("2025-01", "2026-07")
RETIRED = {"2024-03": "Sat, 01 Feb 2026 00:00:00 GMT"}
SUNSET_2025_01 = "Sat, 01 Feb 2027 00:00:00 GMT"

TASK_2025_01 = {
    "id": "T-301",
    "title": "Integrate payment gateway",
    "status": "in_progress",
    "project_id": "P-12",
    "assignee_id": "U-42",
    "due_date": "2026-08-15",
}

TASK_2026_07 = {
    "id": "T-301",
    "title": "Integrate payment gateway",
    "status": "in_progress",
    "project_id": "P-12",
    "assignee_id": "U-42",  # dual-shipped during transition
    "assignee": {
        "id": "U-42",
        "name": "Ada Chen",
        "email": "ada.chen@taskflow.dev",
    },
    "due_date": "2026-08-15",
    "story_points": 8,
}

VALID_STATUSES = ("todo", "in_progress", "done")


class TaskFlowHandler(BaseHTTPRequestHandler):
    server_version = "TaskFlow/1.4"

    def log_message(self, *args):  # silence request logs in tests
        pass

    # -- helpers -----------------------------------------------------
    def _send_json(self, status, payload, headers=None):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _error(self, status, code, message, details=None):
        self._send_json(status, {"error": {"code": code, "message": message,
                                           "details": details or []}})

    def _version(self):
        """Resolve the requested contract from the API-Version header."""
        v = self.headers.get("API-Version")
        if v is None:
            return "2025-01", None          # missing -> stable default
        if v in RETIRED:
            return v, "retired"             # sunset enforced
        if v not in SUPPORTED:
            return v, "unsupported"
        return v, None

    def _common_headers(self, version):
        h = {
            "X-RateLimit-Limit": "120",
            "X-RateLimit-Remaining": "119",
            "X-RateLimit-Reset": "1750108800",
        }
        if version == "2025-01":
            h["Sunset"] = SUNSET_2025_01
        if version == "2026-07":
            h["Deprecation"] = "true"       # legacy field still shipped
        return h

    # -- routes ------------------------------------------------------
    def do_GET(self):
        if not self._check_auth():
            return
        version, problem = self._version()
        if problem == "retired":
            return self._retired(version)
        if problem == "unsupported":
            return self._error(
                400, "unsupported_version",
                f"API-Version '{version}' is not supported.",
                [{"supported": list(SUPPORTED)}],
            )
        path = self.path.split("?")[0]
        if path in ("/v1/tasks/T-301", "/tasks/T-301"):
            task = TASK_2025_01 if version == "2025-01" else TASK_2026_07
            self._send_json(200, task, self._common_headers(version))
        elif path in ("/v1/tasks", "/tasks", "/v1/projects", "/projects"):
            task = TASK_2025_01 if version == "2025-01" else TASK_2026_07
            self._send_json(
                200,
                {"items": [task], "page": 1, "limit": 20, "total": 1},
                self._common_headers(version),
            )
        else:
            self._error(404, "not_found", f"No route for {path}")

    def do_POST(self):
        if not self._check_auth():
            return
        version, problem = self._version()
        if problem == "retired":
            return self._retired(version)
        if problem == "unsupported":
            return self._error(
                400, "unsupported_version",
                f"API-Version '{version}' is not supported.",
                [{"supported": list(SUPPORTED)}],
            )
        body = self._read_json()
        if body is None:
            return self._error(400, "invalid_json", "Request body is not valid JSON.")
        if version == "2026-07" and "project_id" not in body:
            return self._error(
                422, "validation_failed", "project_id is required.",
                [{"field": "project_id", "issue": "required"}],
            )
        headers = self._common_headers(version)
        if version == "2026-07" and "assignee_id" in body:
            headers["Deprecation"] = "true"  # old-client write mapped
        created = dict(body)
        created.setdefault("id", "T-302")
        self._send_json(201, created, headers)

    def do_PATCH(self):
        if not self._check_auth():
            return
        version, problem = self._version()
        if problem == "retired":
            return self._retired(version)
        if problem == "unsupported":
            return self._error(400, "unsupported_version",
                               f"API-Version '{version}' is not supported.")
        body = self._read_json()
        if body is None:
            return self._error(400, "invalid_json", "Request body is not valid JSON.")
        status = body.get("status")
        if status is not None and status not in VALID_STATUSES:
            return self._error(
                422, "validation_failed",
                f"status '{status}' is not allowed.",
                [{"allowed": list(VALID_STATUSES)}],
            )
        task = TASK_2025_01 if version == "2025-01" else TASK_2026_07
        updated = dict(task, **body)
        self._send_json(200, updated, self._common_headers(version))

    def do_DELETE(self):
        if not self._check_auth():
            return
        self.send_response(204)
        self.send_header("Content-Length", "0")
        self.end_headers()

    # -- internals ---------------------------------------------------
    def _check_auth(self):
        token = self.headers.get("Authorization", "")
        if not token.startswith("Bearer "):
            self._error(401, "unauthenticated", "Bearer token required.")
            return False
        if token.endswith("expired"):
            self._error(401, "token_expired", "Bearer token expired.")
            return False
        return True

    def _read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length == 0:
            return {}
        try:
            return json.loads(self.rfile.read(length))
        except json.JSONDecodeError:
            return None

    def _retired(self, version):
        self._send_json(
            410,
            {"error": {"code": "version_retired",
                       "message": f"API-Version '{version}' was retired on "
                                  f"{RETIRED[version]}; migrate to {SUPPORTED[-1]}.",
                       "details": []}},
            {"Link": f"</v1>; rel=\"successor-version\"",
             "Sunset": RETIRED[version]},
        )


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8571
    HTTPServer(("127.0.0.1", port), TaskFlowHandler).serve_forever()
