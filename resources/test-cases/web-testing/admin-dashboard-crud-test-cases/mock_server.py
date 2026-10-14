"""TaskFlow admin API mock — stdlib only.

Implements the fictional TaskFlow admin API from
https://qapractices.com/test-cases/admin-dashboard-crud-test-cases/

Endpoints under /api/v1/{projects,users,tasks} plus /audit-log and
/users/bulk-delete. Every mutation requires a Bearer admin token and the
X-CSRF-Token header; a viewer token can read but gets 403 on writes.

Usage:
    python mock_server.py 8080
"""

import json
import sys
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

TOKENS = {"Bearer ADMIN_TOKEN": "admin", "Bearer VIEWER_TOKEN": "viewer"}
CSRF_TOKEN = "csrf-token-123"
MAX_NAME_LENGTH = 100

STORE = {
    "projects": {},
    "users": {},
    "tasks": {},
}
AUDIT_LOG = []


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def reset_store():
    STORE["projects"] = {
        "PROJ-001": {
            "id": "PROJ-001", "name": "Project Alpha", "code": "PROJ-001",
            "status": "active", "version": 1, "deletedAt": None,
            "createdAt": "2026-07-20T08:00:00Z", "updatedAt": "2026-07-25T12:00:00Z",
        },
    }
    STORE["users"] = {
        "luis.herrera@taskflow.io": {
            "id": "luis.herrera@taskflow.io", "name": "Luis Herrera",
            "email": "luis.herrera@taskflow.io", "role": "viewer",
            "active": True, "version": 1, "deletedAt": None,
            "createdAt": "2026-07-20T08:00:00Z", "updatedAt": "2026-07-25T12:00:00Z",
        },
    }
    STORE["tasks"] = {
        "T-301": {
            "id": "T-301", "title": "Integrate payment gateway", "code": "T-301",
            "projectCode": "PROJ-001", "status": "todo",
            "assigneeEmail": None, "version": 1, "deletedAt": None,
            "createdAt": "2026-07-25T12:00:00Z", "updatedAt": "2026-07-25T12:00:00Z",
        },
    }
    AUDIT_LOG.clear()


def audit(admin, action, entity, entity_id, changes):
    AUDIT_LOG.append({
        "admin": admin, "action": action, "entity": entity,
        "entityId": entity_id, "changes": changes, "timestamp": now_iso(),
    })


def json_body(handler):
    length = int(handler.headers.get("Content-Length") or 0)
    if not length:
        return {}
    try:
        return json.loads(handler.rfile.read(length))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


class Handler(BaseHTTPRequestHandler):
    server_version = "TaskFlowMock/1.0"

    def log_message(self, *args):
        pass

    def respond(self, status, body=None):
        payload = json.dumps(body if body is not None else {}).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def actor(self):
        return TOKENS.get(self.headers.get("Authorization", ""))

    def guard_write(self):
        """Returns an error response tuple or None when the write is allowed."""
        role = self.actor()
        if role is None:
            return (401, {"error": "Authentication required."})
        if role != "admin":
            return (403, {"error": "Forbidden."})
        if self.headers.get("X-CSRF-Token") != CSRF_TOKEN:
            return (403, {"error": "Invalid CSRF token."})
        return None

    def collection(self, path_parts):
        # /api/v1/{projects|users|tasks}[/id]
        if len(path_parts) < 3 or path_parts[2] not in STORE:
            return None, None
        return path_parts[2], (path_parts[3] if len(path_parts) > 3 else None)

    def do_GET(self):
        parsed = urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]
        query = parse_qs(parsed.query)

        if parts == ["api", "v1", "audit-log"]:
            self.respond(200, {"entries": list(reversed(AUDIT_LOG))})
            return

        coll, record_id = self.collection(parts)
        if coll is None:
            self.respond(404, {"error": "Not found."})
            return

        if self.actor() is None:
            self.respond(401, {"error": "Authentication required."})
            return

        store = STORE[coll]
        include_deleted = query.get("include_deleted", ["false"])[0] == "true"

        if record_id:
            record = store.get(record_id)
            if not record or (record["deletedAt"] and not include_deleted):
                self.respond(404, {"error": "Not found."})
                return
            self.respond(200, record)
            return

        rows = [r for r in store.values() if include_deleted or not r["deletedAt"]]
        search = query.get("search", [None])[0]
        if search:
            rows = [r for r in rows if search.lower() in json.dumps(r).lower()]
        rows.sort(key=lambda r: r["createdAt"], reverse=True)

        limit = int(query.get("limit", ["25"])[0])
        page = int(query.get("page", ["1"])[0])
        total = len(rows)
        start = (page - 1) * limit
        self.respond(200, {
            "data": rows[start:start + limit],
            "total": total, "page": page, "limit": limit,
        })

    def do_POST(self):
        err = self.guard_write()
        if err:
            self.respond(*err)
            return
        parsed = urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]
        body = json_body(self)
        if body is None:
            self.respond(400, {"error": "Malformed JSON."})
            return

        if parts == ["api", "v1", "users", "bulk-delete"]:
            ids = body.get("ids", [])
            deleted, errors = [], []
            for uid in ids:
                rec = STORE["users"].get(uid)
                if rec and not rec["deletedAt"]:
                    rec["deletedAt"] = now_iso()
                    rec["version"] += 1
                    deleted.append(uid)
                    audit("admin", "delete", "users", uid, {"deletedAt": rec["deletedAt"]})
                else:
                    errors.append({"id": uid, "error": "Not found or already deleted."})
            self.respond(202, {"deleted": len(deleted), "errors": errors})
            return

        coll, _ = self.collection(parts)
        if coll is None or len(parts) != 3:
            self.respond(404, {"error": "Not found."})
            return

        # validation shared by projects/users/tasks
        if "name" in body and not body["name"]:
            self.respond(400, {"error": "Name is required."})
            return
        if "name" in body and len(body["name"]) > MAX_NAME_LENGTH:
            self.respond(400, {"error": "Name exceeds 100 characters."})
            return

        if coll == "projects":
            code = body.get("code") or "PROJ-%s" % uuid.uuid4().hex[:3].upper()
            if any(r["code"] == code and not r["deletedAt"] for r in STORE[coll].values()):
                self.respond(409, {"error": "Project code %s already exists." % code})
                return
            record = {
                "id": code, "name": body.get("name"), "code": code,
                "status": body.get("status", "active"), "version": 1,
                "deletedAt": None, "createdAt": now_iso(), "updatedAt": now_iso(),
            }
        elif coll == "users":
            email = body.get("email")
            if not email:
                self.respond(400, {"error": "Email is required."})
                return
            if email in STORE[coll] and not STORE[coll][email]["deletedAt"]:
                self.respond(409, {"error": "User %s already exists." % email})
                return
            record = {
                "id": email, "name": body.get("name"), "email": email,
                "role": body.get("role", "viewer"), "active": True, "version": 1,
                "deletedAt": None, "createdAt": now_iso(), "updatedAt": now_iso(),
            }
        else:  # tasks
            project = STORE["projects"].get(body.get("projectCode", ""))
            if not project or project["deletedAt"]:
                self.respond(422, {"error": "Project does not exist."})
                return
            status = body.get("status", "todo")
            if status not in ("todo", "in_progress", "on_hold", "done"):
                self.respond(400, {"error": "Status is not valid."})
                return
            code = body.get("code") or "T-%s" % uuid.uuid4().hex[:3].upper()
            record = {
                "id": code, "title": body.get("title"), "code": code,
                "projectCode": project["id"], "status": status,
                "assigneeEmail": body.get("assigneeEmail"), "version": 1,
                "deletedAt": None, "createdAt": now_iso(), "updatedAt": now_iso(),
            }

        STORE[coll][record["id"]] = record
        audit("admin", "create", coll, record["id"], record)
        self.respond(201, record)

    def do_PATCH(self):
        err = self.guard_write()
        if err:
            self.respond(*err)
            return
        parts = [p for p in urlparse(self.path).path.split("/") if p]
        coll, record_id = self.collection(parts)
        record = coll and STORE[coll].get(record_id)
        if not record or record["deletedAt"]:
            self.respond(404, {"error": "Not found."})
            return
        body = json_body(self)
        if body is None:
            self.respond(400, {"error": "Malformed JSON."})
            return

        if "status" in body and body["status"] not in (
            "active", "on_hold", "todo", "in_progress", "done"
        ):
            self.respond(400, {"error": "Status is not valid."})
            return
        if body.get("version") != record["version"]:
            self.respond(409, {"error": "Version conflict — record was modified."})
            return

        changes = {}
        for field in ("name", "status", "role", "title", "assigneeEmail", "active"):
            if field in body:
                changes[field] = {"old": record[field], "new": body[field]}
                record[field] = body[field]
        record["version"] += 1
        record["updatedAt"] = now_iso()
        audit("admin", "update", coll, record_id, changes)
        self.respond(200, record)

    def do_DELETE(self):
        err = self.guard_write()
        if err:
            self.respond(*err)
            return
        parts = [p for p in urlparse(self.path).path.split("/") if p]
        coll, record_id = self.collection(parts)
        record = coll and STORE[coll].get(record_id)
        if not record or record["deletedAt"]:
            self.respond(404, {"error": "Not found."})
            return

        if coll == "projects":
            linked = [t for t in STORE["tasks"].values()
                      if t["projectCode"] == record_id and not t["deletedAt"]]
            if linked:
                self.respond(422, {"error": "Cannot delete project with associated tasks."})
                return

        record["deletedAt"] = now_iso()
        record["version"] += 1
        audit("admin", "delete", coll, record_id, {"deletedAt": record["deletedAt"]})
        self.respond(200, {"id": record_id, "deletedAt": record["deletedAt"]})


def main():
    reset_store()
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print("TaskFlow admin API mock on http://127.0.0.1:%d" % port)
    print("Auth: Authorization: Bearer ADMIN_TOKEN  +  X-CSRF-Token: %s" % CSRF_TOKEN)
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
