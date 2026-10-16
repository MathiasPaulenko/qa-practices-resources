"""Append-only audit log with SHA-256 hash chaining, backed by sqlite3.

Companion to https://qapractices.com/test-cases/audit-log-activity-history-test-cases/

Every entry embeds the hash of the previous entry (hash_n = sha256(hash_n-1 +
canonical entry fields)). Editing or deleting a row through tamper() — the test
backdoor — breaks the chain and verify_chain() returns the first invalid index.

Deliberately never stores passwords/tokens: append() scrubs sensitive keys at
the logging layer, matching the "exclude sensitive data by default" practice.
"""

import csv
import hashlib
import io
import json
import sqlite3
import threading
from datetime import datetime, timezone
from typing import Optional

SENSITIVE_KEYS = {"password", "passwd", "token", "secret", "api_key", "ssn"}
GENESIS_HASH = "0" * 64


class AuditLog:
    def __init__(self, db_path: str = ":memory:"):
        # check_same_thread=False because TC021 hammers the log from a pool.
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self._lock = threading.Lock()
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                user_id TEXT NOT NULL,
                action TEXT NOT NULL,
                resource TEXT,
                timestamp TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                tenant_id TEXT,
                details TEXT,
                deleted_user INTEGER NOT NULL DEFAULT 0,
                on_hold INTEGER NOT NULL DEFAULT 0,
                prev_hash TEXT NOT NULL,
                hash TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    @staticmethod
    def _canonical(row: dict) -> bytes:
        return json.dumps(row, sort_keys=True, ensure_ascii=False).encode("utf-8")

    @staticmethod
    def _entry_hash(prev_hash: str, fields: dict) -> str:
        return hashlib.sha256(prev_hash.encode() + AuditLog._canonical(fields)).hexdigest()

    @staticmethod
    def _scrub(details: Optional[dict]) -> Optional[str]:
        """Drop sensitive keys at the logging layer, not at query time."""
        if not details:
            return None
        clean = {k: v for k, v in details.items() if k.lower() not in SENSITIVE_KEYS}
        return json.dumps(clean, ensure_ascii=False) if clean else None

    def append(
        self,
        event_type: str,
        user_id: str,
        action: str,
        resource: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        tenant_id: Optional[str] = None,
        details: Optional[dict] = None,
        timestamp: Optional[datetime] = None,
    ) -> int:
        ts = (timestamp or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat()
        fields = {
            "event_type": event_type,
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "timestamp": ts,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "tenant_id": tenant_id,
            "details": self._scrub(details),
        }
        with self._lock:
            prev = self.conn.execute(
                "SELECT hash FROM audit_log ORDER BY id DESC LIMIT 1"
            ).fetchone()
            prev_hash = prev[0] if prev else GENESIS_HASH
            entry_hash = self._entry_hash(prev_hash, fields)
            cur = self.conn.execute(
                """INSERT INTO audit_log
                   (event_type, user_id, action, resource, timestamp, ip_address,
                    user_agent, tenant_id, details, prev_hash, hash)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (*fields.values(), prev_hash, entry_hash),
            )
            self.conn.commit()
            return cur.lastrowid

    def verify_chain(self) -> dict:
        """Recompute the whole chain. Returns first invalid index or None."""
        rows = self.conn.execute(
            """SELECT id, event_type, user_id, action, resource, timestamp,
                      ip_address, user_agent, tenant_id, details, prev_hash, hash
               FROM audit_log ORDER BY id"""
        ).fetchall()
        prev_hash = GENESIS_HASH
        for i, row in enumerate(rows):
            fields = {
                "event_type": row[1], "user_id": row[2], "action": row[3],
                "resource": row[4], "timestamp": row[5], "ip_address": row[6],
                "user_agent": row[7], "tenant_id": row[8], "details": row[9],
            }
            if row[10] != prev_hash or self._entry_hash(prev_hash, fields) != row[11]:
                return {"chainValid": False, "entriesVerified": i, "firstInvalidIndex": row[0]}
            prev_hash = row[11]
        return {"chainValid": True, "entriesVerified": len(rows), "firstInvalidIndex": None}

    def filter(self, user_id=None, action=None, start=None, end=None, limit=50, offset=0):
        where, params = [], []
        if user_id:
            where.append("user_id = ?"); params.append(user_id)
        if action:
            where.append("action = ?"); params.append(action)
        if start:
            where.append("timestamp >= ?"); params.append(start)
        if end:
            # A bare YYYY-MM-DD end date means the whole day — TC011 boundary.
            params.append(end + "T23:59:59.999999" if "T" not in end else end)
            where.append("timestamp <= ?")
        clause = " WHERE " + " AND ".join(where) if where else ""
        total = self.conn.execute(
            f"SELECT COUNT(*) FROM audit_log{clause}", params
        ).fetchone()[0]
        rows = self.conn.execute(
            f"SELECT * FROM audit_log{clause} ORDER BY id LIMIT ? OFFSET ?",
            (*params, limit, offset),
        ).fetchall()
        return {"rows": rows, "totalItems": total}

    def export_csv(self) -> str:
        out = io.StringIO()
        writer = csv.writer(out)
        cols = [c[1] for c in self.conn.execute("PRAGMA table_info(audit_log)").fetchall()]
        writer.writerow(cols)
        writer.writerows(self.conn.execute("SELECT * FROM audit_log ORDER BY id"))
        return out.getvalue()

    def apply_retention(self, cutoff_iso: str) -> int:
        """Delete entries older than the cutoff unless the user is on legal hold."""
        cur = self.conn.execute(
            "DELETE FROM audit_log WHERE timestamp < ? AND on_hold = 0", (cutoff_iso,)
        )
        self.conn.commit()
        return cur.rowcount

    def set_legal_hold(self, user_id: str, held: bool = True):
        self.conn.execute(
            "UPDATE audit_log SET on_hold = ? WHERE user_id = ?", (1 if held else 0, user_id)
        )
        self.conn.commit()

    def delete_user(self, user_id: str):
        """GDPR-style deletion: entries stay, the user is marked as deleted."""
        self.conn.execute(
            "UPDATE audit_log SET deleted_user = 1 WHERE user_id = ?", (user_id,)
        )
        self.conn.commit()

    def tamper(self, row_id: int, field: str, value: str):
        """TEST BACKDOOR — a direct UPDATE that skips the chain. TC018 bait."""
        self.conn.execute(
            f"UPDATE audit_log SET {field} = ? WHERE id = ?", (value, row_id)
        )
        self.conn.commit()
